from flask import Flask, request, jsonify, render_template
from src.helper import download_embeddings, text_chunk
import os
from dotenv import load_dotenv
from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate 
from src.prompt import *
from src.helper import embeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embeddings = download_embeddings("sentence-transformers/all-MiniLM-L6-v2")

index_name = "medical-assistance-chatbot"
vector_store=PineconeVectorStore.from_documents(
    documents=text_chunk,
    embedding=embeddings,
    index_name=index_name
    )

retriver=vector_store.as_retriever(search_type="similarity", search_kwargs={"k":3})
from langchain_google_genai import ChatGoogleGenerativeAI
chatModel=ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GOOGLE_API_KEY)

prompt=ChatPromptTemplate.from_messages(
    ["system",system_prompt,
    "human","{input}"]
    )

question_answer_chain=create_stuff_documents_chain(chatModel,prompt)
rag_chain=create_retrieval_chain(retriver,question_answer_chain)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"]) 

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=3000, debug=True)

