from dotenv import load_dotenv
import voyageai
import numpy as np
import re

load_dotenv()

voyage_client = voyageai.Client()

def chunk_by_section(text):
    sections = re.split(r"\n## ", text)
    return [section.strip() for section in sections if section.strip()]

def generate_embedding(texts, input_type="document"):
    if isinstance(texts, str):
        texts = [texts]

    result = voyage_client.embed(
        texts,
        model="voyage-3-large",
        input_type=input_type
    )

    return result.embeddings

def cosine_distance(a, b):
    a = np.array(a)
    b = np.array(b)

    similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    distance = 1 - similarity

    return distance

class VectorIndex:
    def __init__(self):
        self.vectors = []

    def add_vector(self, embedding, metadata):
        self.vectors.append({
            "embedding": embedding,
            "metadata": metadata
        })

    def search(self, query_embedding, top_k=2):
        results = []

        for item in self.vectors:
            distance = cosine_distance(query_embedding, item["embedding"])
            results.append((item["metadata"], distance))

        results.sort(key=lambda x: x[1])

        return results[:top_k]

# Step 1: Load report
with open("report.md", "r", encoding="utf-8") as f:
    text = f.read()

# Step 2: Chunk report
chunks = chunk_by_section(text)

print("Total chunks:", len(chunks))

# Step 3: Generate embeddings
embeddings = generate_embedding(chunks, input_type="document")

# Step 4: Store in vector index
store = VectorIndex()

for embedding, chunk in zip(embeddings, chunks):
    store.add_vector(embedding, {"content": chunk})

# Step 5: Search with user question
question = "What did the software engineering department do last year?"

query_embedding = generate_embedding(question, input_type="query")[0]

results = store.search(query_embedding, top_k=2)

print("\nSearch Results:\n")

for doc, distance in results:
    print("Distance:", distance)
    print(doc["content"][:300])
    print("-" * 50)