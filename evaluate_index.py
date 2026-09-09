import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
import shutil
import sys

load_dotenv()

llm = OpenAILike(
    model="anthropic/claude-sonnet-4",
    api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    is_chat_model=True,
    max_tokens=500,
)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = llm
Settings.embed_model = embed_model

# --- Step 1: Naya index build karo test location pe (production ko touch nahi karte abhi) ---
print("Naya index build ho raha hai (staging)...")
documents = SimpleDirectoryReader("data").load_data()

chroma_client = chromadb.PersistentClient(path="./chroma_db_staging")
chroma_collection = chroma_client.get_or_create_collection("pdf_collection_staging")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine(similarity_top_k=3)

# --- Step 2: Evaluation set — sawal + expected keywords ---
eval_set = [
    {"question": "who are the supervisors", "expected_keywords": ["Adel Bibi", "Philip Torr"]},
    {"question": "what programming language is used", "expected_keywords": ["Python"]},
]

# --- Step 3: Har sawal test karo ---
passed = 0
failed = 0

for item in eval_set:
    response = str(query_engine.query(item["question"]))
    found = any(kw.lower() in response.lower() for kw in item["expected_keywords"])

    if found:
        print(f"✅ PASS: '{item['question']}'")
        passed += 1
    else:
        print(f"❌ FAIL: '{item['question']}' — expected keywords not found")
        print(f"   Got: {response[:150]}")
        failed += 1

print(f"\nResults: {passed} passed, {failed} failed")

# --- Step 4: Gate decision ---
if failed == 0:
    print("✅ Evaluation PASSED — index deploy ke liye ready hai")
    # Staging ko production mein promote karo
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
    shutil.copytree("./chroma_db_staging", "./chroma_db")
    print("Index production mein promote ho gaya!")
    sys.exit(0)
else:
    print("❌ Evaluation FAILED — deployment ROKA gaya. Production index unchanged.")
    sys.exit(1)