from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader,
    CSVLoader,
    DirectoryLoader
)

# Load text files from a directory
dir_loader = DirectoryLoader("./data/", glob="**/*.txt")
# Load the documents from the directory
dir_documents = dir_loader.load()

print("Loaded documents from directory:", dir_documents)

