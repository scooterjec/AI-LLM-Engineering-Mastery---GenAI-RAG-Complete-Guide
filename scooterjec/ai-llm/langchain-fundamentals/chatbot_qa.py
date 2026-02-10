from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import SeleniumURLLoader

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from typing import Dict, List

model = init_chat_model("llama3.2", model_provider = "ollama")

# List of docs to load
documents = [
    "https://beebom.com/what-is-nft-explained/",
    "https://beebom.com/how-delete-servers-discord/",
    "https://beebom.com/how-list-groups-linux/",
    "https://beebom.com/how-open-port-linux/",
    "https://beebom.com/linux-vs-windows/"
]

def scrape_docs(urls: List[str]) -> List[Dict]:
    """Scrape content from URLs using SeleniumURLLoader."""
    try:
        loader = SeleniumURLLoader(urls)
        raw_docs = loader.load()
        print(f"\nSuccessfully loaded {len(raw_docs)} documents.")

        # Print some info about the loaded documents
        for doc in raw_docs:
            print(f"\nSource: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content length: {len(doc.page_content)} characters")

        return raw_docs
    except Exception as e:
        print(f"\nError loading documents: {e}")
        return []

def create_vector_store(texts: List[str], metadatas: List[Dict]):
    """Create vector store using ChromaDB."""
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    db = Chroma.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    return db

def setup_qa_chain(db):
    """Set up QA chain with polite response template."""
    llm = init_chat_model("llama3.2", model_provider = "ollama", temperature=0)
    retriever = db.as_retriever()

    #Create a custom prompt template
    prompt = ChatPromptTemplate.from_template(
        """
        Please provide a polite and helpful response to the following question, utilizing the provided context. 
        Ensure that the tone remains professional, courteous and empathetic, and tailor your response to directly address the inquiry.

        ### Context:
        {context}

        ### Question:
        {question}
        
        ### Polite response:
        In your response, consider including:
        - Acknowledge the user's question and express willingness to assist.
        - Provide a clear and concise answer that directly addresses the user's inquiry.
        - Use positive language and mantain a supportive tone throughout the response.
        - If applicable, include relevant information or resources that could help further.
        - Conclude by inviting any follow-up questions or providing encouragement for the user's pursuit of information.
        """
    )

    # Create the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever

def split_documents(pages_content: List[Dict]) -> tuple:
    """Split documents into chunks"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_texts, all_metadatas = [], []

    for doc in pages_content:
        # Extract text from Document object
        text = doc.page_content
        source = doc.metadata.get("source", "Unknown")

        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            all_texts.append(chunk)
            all_metadatas.append({"source": source})

    print(f"\nTotal chunks created: {len(all_texts)}")

    return all_texts, all_metadatas

def process_query(chain_and_retriever, query: str):
    """Process a query and return response"""
    try:
        chain, retriever = chain_and_retriever

        #Get the response
        response = chain.invoke(query)

        # Get the sources using the retriever
        docs = retriever.invoke(query)
        sources_str = ", ".join([doc.metadata.get("source", "") for doc in docs])

        return {"answer": response, "sources": sources_str}
    except Exception as e:
        print(f"\nError processing query: {e}")
        return {"answer": "Sorry, I couldn't process your query at the moment.", "sources": ""}

def main():
    # 1. Scrape the documents
    print("Scraping documents...")
    pages_content = scrape_docs(documents)

    # 2. Split socuments
    print("\nSplitting documents...")
    all_texts, all_metadatas = split_documents(pages_content)

    # 3. Create vector store
    print("\nCreating vector store...")
    db = create_vector_store(all_texts, all_metadatas)

    # 4. Set up QA chain
    print("\nSetting up QA chain...")
    qa_chain = setup_qa_chain(db)

    # 5. Interactive query loop
    print("\nYou can now ask questions about the loaded documents. Type 'quit' to exit.")
    while True:
        query = input("\nEnter your question: ").strip()
        if not query:
            print("Please enter a valid question.")
            continue
        if query.lower() == "quit":
            print("Exiting. Goodbye!")
            break

        result = process_query(qa_chain, query)
        print(f"\nAnswer: {result['answer']}")

        if result["sources"]:
            print("\nSources:")
            for source in result["sources"].split(", "):
                print(f"- {source.strip()}")


if __name__ == "__main__":
    main()


