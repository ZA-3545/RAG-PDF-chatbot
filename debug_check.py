from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()

print(f"Total documents: {len(documents)}")
for i, doc in enumerate(documents):
    print(f"\n--- Document {i+1} ---")
    print(f"Text length: {len(doc.text)} characters")
    print(f"First 300 characters:\n{doc.text[:300]}")