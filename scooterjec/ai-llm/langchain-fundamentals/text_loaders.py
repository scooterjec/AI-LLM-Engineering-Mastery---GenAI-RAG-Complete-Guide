from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import pprint

# Data cleaning function
def clean_text(text):
    # Remove unwanted characters, extra spaces, etc.
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Keep only letters and spaces
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text.lower()  # Convert to lowercase



documents = TextLoader("./doc/dream.txt").load()

# Clean the text
cleaned_documents = [clean_text(doc.page_content) for doc in documents]
# print(cleaned_documents[:10])  # Print the first 10 cleaned documents

# Split the text into characters
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# texts = text_splitter.split_text(cleaned_document[0])  # Assuming cleaned_document is a list of strings
texts = text_splitter.split_documents(documents)  # Assuming cleaned_document is a list of strings

# cleanup text
texts = [clean_text(text.page_content) for text in texts]
# print(texts[:10])  # Print the first 10 split texts

# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Create the retriever from the loaded embeedings and documents
retriever = FAISS.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 2})

# Query the retriever
query = "What did Martin Luther King Jr. dream about?"
docs = retriever.invoke(query)

pprint.pprint(f" => DOCS: {docs}")

# Chat with the model and our docs

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


# # Create the chat prompt
prompt = ChatPromptTemplate.from_template(
    "Please use the following docs {docs},and answer the following question {query}",
)

# # Create a chat model
# model = ChatOpenAI(model="gpt-4o-mini")
from langchain.chat_models import init_chat_model
model = init_chat_model("llama3.2", model_provider = "ollama")

chain = prompt | model | StrOutputParser()

query = "Give me a summary of the speech in bullet points and translate them to Spanish"
response = chain.invoke({"docs": docs, "query": query})
print(f"\n\nModel Response::: \n \n{response}")
 
