from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader,
    CSVLoader,
    DirectoryLoader
)

# Load a PDF file
pdf_loader = PyPDFLoader("./doc/linux-manual.pdf")

# Load the document from the PDF file
docs = pdf_loader.load()

print("Loaded documents from PDF:", docs)
