import streamlit as st
import whisper
import sounddevice as sd
import soundfile as sf
from elevenlabs.client import ElevenLabs

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader,
    UnstructuredMarkdownLoader,
    DirectoryLoader
)

import tempfile
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " ", ""])
        self.embeddings = OpenAIEmbeddings()

    def load_documents(self, directory: str) -> List[Document]:
        """Load documents from different file types"""
        loader = {
            ".pdf": DirectoryLoader(directory, glob="**/*.pdf", loader_cls = PyPDFLoader, show_progress=True),
            ".txt": DirectoryLoader(directory, glob="**/*.txt", loader_cls = TextLoader , show_progress=True),
            ".md":  DirectoryLoader(directory, glob="**/*.md", loader_cls = UnstructuredMarkdownLoader, show_progress=True),
        }

        documents = []
        for file_type., loader in loader.items():
            try:
                documents.extend(loader.load())
                print(f"Loaded {file_type} documents from {directory}")
            except Exception as e:
                print(f"Error loading {file_type} documents: {str(e)}")

        return documents

    def process_documents(self, documents: List[Document]) -> List[Documents]:
        """Split documents into chunks"""
        return self.text_splitter.split_documents(documents)

    def create_vector_store(self, documents: List[Document], persist_directory: str) -> Chroma:
        """Create and persist vector store if it doesn't exist, otherwise load existing store"""
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            print("Loading existing vector store...")
            vector_store =  Chroma(persist_directory=persist_directory, embedding_function=self.embeddings)
        else:
            print("Creating new vector store...")
            os.makedirs(persist_directory, exist_ok=True)
            vector_store = Chroma.from_documents(documents, self.embeddings, persist_directory=persist_directory)
            vector_store.persist()
            
        return vector_store

class VoiceGenerator:
    def __init__(self, api_key: str):
        self.client = ElevenLabs(api_key=os.getenv("ELEVEN_LAVS_API_KEY"))
        self.avilable_voices = ["Rachel","Domi","Antoni","Elli","Josh","Arnold","Adam","Sam","Bella"]
        self.default_voice = "Rachel"

    def generate_voice(self, text: str, voice_name: str = None):
        """Generate voice response"""
        try:
            selected_voice = voice_name or self.default_voice

            # Generate audio using the client
            audio_generator = self.client.generate(
                text=text,
                voice=selected_voice,
                model="eleven_multilingual_v1",
            )

            # Convert generator to bytes
            audio_bytes = b"".join(audio_generator)

            # Save to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(audio_bytes)
                return temp_audio_file.name

        except Exception as e:
            print(f"Error generating voice: {str(e)}")
            return None

class VoiceAssistantRAG:
    def __init__(self, elevenlabs_api_key: str):
        self,whisper_model = whisper.load_model("base")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.qa_chain = None
        self.voice_generator = VoiceGenerator(elevenlabs_api_key)

    def setup_vector_store(self, vector:_store):
        """Initialize vector store and QA chain"""
        self.vector_store = vector_store
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=vector_store.as_retriever(),
            memory=memory,
            verbose=True
        )

    def record_audio(self, duration=5):
        """Record audio from microphone"""
        recording = sd.rec(int(duration * 44100), samplerate=self.sample_rate, channels=2)
        sd.wait()
        return recording

    def transcribe_audio(self, audio_array):
        """Transcribe audio using Whisper model"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            sf.write(temp_audio_file.name, audio_array, self.sample_rate)
            result = self.whisper_model.transcribe(temp_audio_file.name)
            os.unlink(temp_audio_file.name)
            return result["text"]

    def generate_response(self, query):
        """Generate response using QA chain and return voice response"""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Please set up vector store first.")

        response = self.qa_chain.invoke({"question": query})
        return response["answer"]

    def text_to_speech(self, text, voice_name=None):
        """Convert text response to speech and return audio file path"""
        return self.voice_generator.generate_voice_response(text, voice_name)

def setup_knowledge_base():
    st.title("Knowledge Base setup")
    doc_processor = DocumentProcessor()
    uploaded_files = st.file_uploader("Upload documents (PDF, TXT, MD)", accept_multiple_files=True, type=["pdf", "txt", "md"])
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            temp_dir = tempfile.mkdtemp()
            for file in uploaded_files:
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

            try:
                documents = doc_processor.load_documents(temp_dir)
                processed_docs = doc_processor.process_documents(documents)
                vector_store = doc_processor.create_vector_store(processed_docs, "knowlñedge_base")
                st.session_state.vector_store = vector_store
                st.success("Knowledge base created successfully!")
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")
            finally:
                for file in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file.name))
                os.rmdir(temp_dir)

def main():
    st.set_page_config(page_title="Voice RAG Assistant", layout="wide")

    # Check for API keys
    elevenlabs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([elevenlabs_api_key, openai_api_key]):
        st.error(
            "Please set ELEVEN_LABS_API_KEY and OPENAI_API_KEY in your environment variables"
        )
        return

    # Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Setup Knowledge Base", "Voice Assistant"])

    if page == "Setup Knowledge Base":
        vector_store = setup_knowledge_base()
        if vector_store:
            st.session_state.vector_store = vector_store

    else:  # Voice Assistant page
        if "vector_store" not in st.session_state:
            st.error("Please setup knowledge base first!")
            return

        st.title("Voice Assistant RAG System")

        # Initialize assistant
        assistant = VoiceAssistantRAG(elevenlabs_api_key)
        # Initialize the vector store and QA chain
        assistant.setup_vector_store(st.session_state.vector_store)

        # Voice selection
        try:
            available_voices = assistant.voice_generator.available_voices
            if available_voices:
                selected_voice = st.sidebar.selectbox(
                    "Select Voice",
                    available_voices,
                    index=(
                        available_voices.index("Rachel")
                        if "Rachel" in available_voices
                        else 0
                    ),
                )
            else:
                st.warning("No voices available. Using default voice.")
                selected_voice = "Rachel"
        except Exception as e:
            st.error(f"Error loading voices: {e}")
            selected_voice = "Rachel"

        # Recording duration
        duration = st.sidebar.slider("Recording Duration (seconds)", 1, 10, 5)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Start Recording"):
                with st.spinner(f"Recording for {duration} seconds..."):
                    audio_data = assistant.record_audio(duration)
                    st.session_state.audio_data = audio_data
                    st.success("Recording completed!")

        with col2:
            if st.button("Process Recording"):
                if "audio_data" not in st.session_state:
                    st.error("Please record audio first!")
                    return

                # Process recording
                with st.spinner("Transcribing..."):
                    query = assistant.transcribe_audio(st.session_state.audio_data)
                    st.write("You said:", query)

                with st.spinner("Generating response..."):
                    try:
                        response = assistant.generate_response(query)
                        st.write("Response:", response)
                        st.session_state.last_response = response
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                        return

                with st.spinner("Converting to speech..."):
                    audio_file = assistant.voice_generator.generate_voice_response(
                        response, selected_voice
                    )
                    if audio_file:
                        st.audio(audio_file)
                        os.unlink(audio_file)
                    else:
                        st.error("Failed to generate voice response")

        # Display chat history
        if "chat_history" in st.session_state:
            st.subheader("Chat History")
            for q, a in st.session_state.chat_history:
                st.write("Q:", q)
                st.write("A:", a)
                st.write("---")


if __name__ == "__main__":
    main()
    
