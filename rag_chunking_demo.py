import re

# Read markdown file
with open("report.md", "r", encoding="utf-8") as f:
    text = f.read()

print("\n===== ORIGINAL DOCUMENT =====\n")
print(text)

# Sentence chunking function
def chunk_by_sentence(text, max_sentences=2):

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []

    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        chunks.append(chunk)

    return chunks

# Create chunks
chunks = chunk_by_sentence(text)

print("\n===== GENERATED CHUNKS =====\n")

for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---\n")
    print(chunk)