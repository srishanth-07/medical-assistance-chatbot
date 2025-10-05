#for loading pdfs
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
#for splitting the text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

#load and extract text from pdf files
def load_pdf_file(data):
    if os.path.isdir(data):
        loader = DirectoryLoader(
            data,
            glob="*.pdf",
            loader_cls=PyPDFLoader)
        documents = loader.load()
    else:
        loader = PyPDFLoader(data)
        documents = loader.load()
    return documents

def filter_to_minimalDocs(docs: List[Document]) -> List[Document]:
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

#divide the text into chunks
def text_split(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    text_chunks = text_splitter.split_documents(docs)
    return text_chunks

# Load documents from your PDF folder
pdf_folder_path = "/Users/srishanthreddy/medical-assistance-chatbot/data/Medical_book.pdf"  # <-- update to your actual path
docs = load_pdf_file(pdf_folder_path)

# Filter documents to minimal docs
minimal_docs = filter_to_minimalDocs(docs)

# Split minimal docs into chunks
text_chunk = text_split(minimal_docs)
print(len(text_chunk))

#download embedding model
def download_embeddings(model_name):
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

embeddings = download_embeddings("sentence-transformers/all-MiniLM-L6-v2")