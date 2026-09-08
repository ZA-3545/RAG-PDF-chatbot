import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# .env file se API key load karo
load_dotenv()

# Claude model set karo (OpenRouter ke through)
llm = OpenAILike(
    model="anthropic/claude-sonnet-4",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    is_chat_model=True,
    max_tokens=1000,
)

# Embedding model set karo (local, free — HuggingFace se)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Global settings mein dono set kar do (taake LlamaIndex OpenAI default use na kare)
Settings.llm = llm
Settings.embed_model = embed_model

# 1. PDF(s) load karo "data" folder se
print("PDF load ho rahi hai...")
documents = SimpleDirectoryReader("data").load_data()
print(f"{len(documents)} document(s) load hue.")

# 2. Chroma vector database setup karo (local, persistent)
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("pdf_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 3. Index banao (chunking + embedding + storing automatically ho jayega)
print("Index ban raha hai (chunking + embedding)...")
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
print("Index ban gaya aur 'chroma_db' folder mein save ho gaya!")