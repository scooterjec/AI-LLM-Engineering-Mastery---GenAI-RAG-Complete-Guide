import yt_dlp
import os
import whisper
from typing import Dict, List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv()

class EmbeddingModel:
    """Handles different embedding models"""

    def __init__(self, model_type="openai"):
        self.model_type = model_type
        if model_type == "openai":
            self.embedding_fn = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif model_type == "chroma":
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embedding_fn = HuggingFaceEmbeddings()
        elif model_type == "nomic":
            from langchain_ollama.embeddings import OllamaEmbeddings
            self.embedding_fn = OllamaEmbeddings(
                model="nomic-embed-text",
                base_url="http://localhost:11434"
            )
        else:
            raise ValueError(f"Unsupported embedding model type: {model_type}")

class LLMModel:
    """Handles different LLM Models"""

    def __init__(self, model_type="openai", model_name="gpt-4"):
        self.model_type = model_type
        self.model_name = model_name

        if model_type == "openai":
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY environment variable not set")
            self.llm = ChatOpenAI(model=model_name, temperature=0)
        elif model_type == "ollama":
            self.llm = ChatOllama(model=model_name, base_url="http://localhost:11434", temperature=0, format="json", timeout=120)
        else:
            raise ValueError(f"Unsupported LLM model type: {model_type}")

class YouTubeVideoSummarizer:

    def __init__(self, llm_type="openai", llm_model_name="gpt-4", embedding_type="openai"):
        """Initialize with different LLM and embedding options"""
        # Initialize models
        self.embedding_model = EmbeddingModel(model_type=embedding_type)
        self.llm_model = LLMModel(model_type=llm_type, model_name=llm_model_name)

        # Initialize whisper
        self.whisper_model = whisper.load_model("base")

    def get_model_info(self) -> Dict:
        """Return information about the models being used"""
        return {
            "llm_type": self.llm_model.model_type,
            "llm_name": self.llm_model.model_name,
            "embedding_type": self.embedding_model.model_type
        }

    def download_video(self, url: str) -> tuple[str, str]:
        """Download video and extract audio"""
        print(f"Downloading video from {url}...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_path = ydl.prepare_filename(info).replace('.webm', '.mp3')
            video_title = info.get('title', 'Unknown Title')
            return audio_path, video_title

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using Whisper"""
        print(f"Transcribing audio from {audio_path}...")
        result = self.whisper_model.transcribe(audio_path)
        return result['text']

    def create_documents(self, text: str, video_title: str) -> List[Document]:
        """Split text into chunks and create Document objects"""
        print("Creating documents from transcribed text...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", ". ", " ", ""])
        texts = text_splitter.split_text(text)
        documents = [Document(page_content=chunk, metadata={"source": video_title}) for chunk in texts]
        return documents

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create a vector store from the documents"""
        print(f"Creating vector store using {self.embedding_model.model_type} embeddings...")
        vector_store = Chroma.from_documents(
                documents=documents, 
                embedding=self.embedding_model.embedding_fn,
                collection_name=f"yt_video_summary_{self.embedding_model.model_type}"
            )
        return vector_store

    def generate_summary(self, documents: List[Document]) -> str:
        """Generate a summary using LangChain's summarize chain"""
        print(f"Generating summary using {self.llm_model.model_type}...")
        map_prompt = ChatPromptTemplate.from_template(
                """Write a concise summary of the following transcript section:
                "{text}"
                CONCISE SUMMARY:"""
            )
        combine_prompt = ChatPromptTemplate.from_template(
                """Write a detailed summary of the following video transcript sections:
                "{text}"

                Include:
                - Main topics and key points
                - Important details and examples
                - Any conclusions or takeaways

                CONCISE SUMMARY:"""
            )

        summary_chain = load_summarize_chain(
                llm =self.llm_model.llm,
                chain_type="map_reduce",
                map_prompt=map_prompt,
                combine_prompt=combine_prompt,
                verbose=True
            )

        return summary_chain.invoke(documents)

    def setup_qa_chain(self, vector_store: Chroma):
        """ Set up question-answering chain"""
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm_model.llm,
            retriever=vector_store.as_retriever(),
            memory=memory,
            verbose=True
        )

    def process_video(self, url: str) -> Dict:
        """Process video and return summary and QA chain"""
        try:
            # Create download dir if it doesn't exist
            os.makedirs("downloads", exist_ok=True)

            # Download and process video
            audio_path, video_title = self.download_video(url)
            transcript = self.transcribe_audio(audio_path)
            documents = self.create_documents(transcript, video_title)
            summary = self.generate_summary(documents)
            vector_store = self.create_vector_store(documents)
            qa_chain = self.setup_qa_chain(vector_store)

            # Clean up
            os.remove(audio_path)

            return {
                    "summary": summary,
                    "qa_chain": qa_chain,
                    "title": video_title,
                    "full_transcript": transcript
                }
        except Exception as e:
            print(f"Error processing video: {e}")
            return {}


def main():
    # Get models preferences
    print("\nWelcome to the YouTube Video Summarizer!")
    print("Available LLM Models: 1) OpenAI , 2) Ollama ")
    llm_choice = input("Choose LLM model (1 or 2): ").strip()

    print("\nAvailable Embedding Models: 1) OpenAI , 2) Chroma (HuggingFace), 3) Nomic (Ollama)")
    embedding_choice = input("Choose embedding model (1, 2, or 3): ").strip()

    # Configure model settings
    llm_type = "openai" if llm_choice == "1" else "ollama"
    llm_model_name = "gpt-4" if llm_choice == "1" else "llama3.2"

    if embedding_choice == "1":
        embedding_type = "openai"
    elif embedding_choice == "2":
        embedding_type = "chroma"
    else:
        embedding_type = "nomic"

    try:
        # Initialize summarizer:
        summarizer = YouTubeVideoSummarizer(llm_type=llm_type, llm_model_name=llm_model_name, embedding_type=embedding_type)

        # Display configuration
        model_info = summarizer.get_model_info()
        print("\n Current configuration:")
        print(f"LLM Model: {model_info['llm_type']} - {model_info['llm_name']}")
        print(f"Embedding Model: {model_info['embedding_type']}")

        # Process video
        video_url = input("\nEnter YouTube video URL to summarize: ").strip()
        result = summarizer.process_video(video_url)

        if result:
            print(f"\nVideo Title: {result['title']}")
            print("\nSummary:")
            print(result['summary'])

            # Interactive Q&A
            print("\nYou can now ask questions about the video content. Type 'quit' to exit.")
            while True:
                query = input("\nYour question: ").strip()
                if query.lower() == "quit":
                    print("Exiting. Thank you for using the YouTube Video Summarizer!")
                    break
                if query:
                    response = result['qa_chain'].invoke({"question": query})
                    print("\nAnswer:", response['answer'])

            # Option to see full transcript
            if input("\nWould you like to see the full transcript? (y/n): ").strip().lower() == "y":
                print("\nFull Transcript:")
                print(result['full_transcript'])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
