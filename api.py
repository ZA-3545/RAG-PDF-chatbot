import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

load_dotenv()

# LLM aur embedding model set karo (query.py jaisa hi)
llm = OpenAILike(
    model="anthropic/claude-sonnet-4",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    is_chat_model=True,
    max_tokens=1000,
)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

# Chroma se index load karo (server start hone pe SIRF EK BAAR)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("pdf_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
index = VectorStoreIndex.from_vector_store(vector_store)
query_engine = index.as_query_engine(similarity_top_k=3)

# FastAPI app banao
app = FastAPI(title="RAG PDF Q&A API")

# Request body ka structure
class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "RAG API is running"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    response = query_engine.query(request.question)

    sources = []
    for node in response.source_nodes:
        sources.append({
            "file_name": node.node.metadata.get("file_name", "Unknown"),
            "score": node.score,
            "snippet": node.node.text[:150]
        })

    return {
        "answer": str(response),
        "sources": sources
    }