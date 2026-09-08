from pypdf import PdfReader

reader = PdfReader("data/agentic-safety-rl-project-plan.pdf")
print(f"Total pages: {len(reader.pages)}")

text = reader.pages[0].extract_text()
print(f"\nPage 1 text (first 300 chars):\n{text[:300]}")