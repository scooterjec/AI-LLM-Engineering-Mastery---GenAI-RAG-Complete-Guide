from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load your document (assuming a text file)
text_loader = TextLoader("./doc/dream.txt")
# Load the document content
documents = text_loader.load()

# Create a text splitter with a specified chunk size and overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20, length_function=len)

# Split the document into chunks
splits = text_splitter.split_documents(documents)
# Print the resulting chunks
for i, split in enumerate(splits):
    print(f"Split {i + 1}:\n{split}\n")


