import os
from dotenv import load_dotenv
from llama_index.llms.anthropic import Anthropic

load_dotenv()

print("API key mili:", os.getenv("ANTHROPIC_API_KEY") is not None)

try:
    llm = Anthropic(model="claude-sonnet-4-6")
    response = llm.complete("Say hello in one sentence.")
    print("Response:", response)
except Exception as e:
    print("ERROR:", e)