from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Sirf embedding model chahiye retrieval test ke liye (LLM ki zaroorat nahi is step mein)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("pdf_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

index = VectorStoreIndex.from_vector_store(vector_store)

retriever = index.as_retriever()
nodes = retriever.retrieve("What is the tech stack used in this project?")

print(f"Retrieved nodes: {len(nodes)}")
for i, node in enumerate(nodes):
    print(f"\n--- Node {i+1} (score: {node.score}) ---")
    print(node.text[:200])