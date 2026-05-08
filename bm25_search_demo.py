import re
from rank_bm25 import BM25Okapi

def chunk_by_section(text):
    sections = re.split(r"\n## ", text)
    return [section.strip() for section in sections if section.strip()]

def tokenize(text):
    return re.findall(r"\b[\w\-]+\b", text.lower())

with open("report.md", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_by_section(text)

tokenized_chunks = [tokenize(chunk) for chunk in chunks]

bm25 = BM25Okapi(tokenized_chunks)

query = "What happened with INC-2023-Q4-011?"
tokenized_query = tokenize(query)

scores = bm25.get_scores(tokenized_query)

results = sorted(
    zip(chunks, scores),
    key=lambda x: x[1],
    reverse=True
)

print("\nBM25 Search Results:\n")

for chunk, score in results[:3]:
    print("Score:", score)
    print(chunk[:400])
    print("-" * 60)