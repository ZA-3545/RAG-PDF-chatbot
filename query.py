import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# .env file se API key load karo
load_dotenv()

# LLM aur embedding model set karo
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

# Pehle se saved Chroma DB ko load karo
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("pdf_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

index = VectorStoreIndex.from_vector_store(vector_store)

# Query engine banao — top 3 chunks retrieve karega (multiple sources ke liye better)
query_engine = index.as_query_engine(similarity_top_k=3)

print("PDF Q&A Chatbot ready hai! ('exit' likh kar band karein)\n")

while True:
    question = input("Aapka sawal: ")
    if question.lower() == "exit":
        print("Bye!")
        break
    if not question.strip():
        print("Sawal khali hai, dobara likhein.\n")
        continue

    response = query_engine.query(question)
    print(f"\nJawab: {response}")

    # Source citation dikhao
    print("\n📄 Sources:")
    for node in response.source_nodes:
        file_name = node.node.metadata.get("file_name", "Unknown")
        score = node.score
        score_str = f"{score:.2f}" if score is not None else "N/A"
        snippet = node.node.text[:100].replace("\n", " ")
        print(f"  - {file_name} (relevance: {score_str}) — \"{snippet}...\"")
    print()