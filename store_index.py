from dotenv import load_dotenv
import os
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from pinecone import Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define embedding model
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define your text chunks (replace with your actual data)
from langchain.schema import Document
from src.helper import text_chunk, embedding  # Import actual data and embedding

# Creating pinecone index
index_name = "medical-assistance-chatbot"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(index_name)

# Store the text chunks in pinecone vector database
vector_store = PineconeVectorStore.from_documents(
    documents=text_chunk,
    embedding=embedding,
    index_name=index_name
)

