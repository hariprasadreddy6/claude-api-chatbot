from dotenv import load_dotenv
import voyageai
import numpy as np
import re
from rank_bm25 import BM25Okapi

load_dotenv()

voyage_client = voyageai.Client()

def chunk_by_section(text):
    sections = re.split(r"\n## ", text)
    return [section.strip() for section in sections if section.strip()]

def tokenize(text):
    return re.findall(r"\b[\w\-]+\b", text.lower())

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
    return 1 - similarity

class VectorIndex:
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        embedding = generate_embedding(document["content"], input_type="document")[0]
        self.documents.append({
            "document": document,
            "embedding": embedding
        })

    def search(self, query_text, k=3):
        query_embedding = generate_embedding(query_text, input_type="query")[0]
        results = []

        for item in self.documents:
            distance = cosine_distance(query_embedding, item["embedding"])
            results.append((item["document"], distance))

        results.sort(key=lambda x: x[1])
        return results[:k]

class BM25Index:
    def __init__(self):
        self.documents = []
        self.tokenized_documents = []
        self.bm25 = None

    def add_document(self, document):
        self.documents.append(document)
        self.tokenized_documents.append(tokenize(document["content"]))
        self.bm25 = BM25Okapi(self.tokenized_documents)

    def search(self, query_text, k=3):
        scores = self.bm25.get_scores(tokenize(query_text))

        results = list(zip(self.documents, scores))
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:k]

class Retriever:
    def __init__(self, *indexes):
        if len(indexes) == 0:
            raise ValueError("At least one index required")
        self.indexes = indexes

    def add_document(self, document):
        for index in self.indexes:
            index.add_document(document)

    def search(self, query_text, k=3, k_rrf=60):
        doc_scores = {}

        for index in self.indexes:
            results = index.search(query_text, k)

            for rank, (doc, _) in enumerate(results, start=1):
                content = doc["content"]

                if content not in doc_scores:
                    doc_scores[content] = {
                        "document": doc,
                        "score": 0
                    }

                doc_scores[content]["score"] += 1 / (k_rrf + rank)

        final_results = list(doc_scores.values())
        final_results.sort(key=lambda x: x["score"], reverse=True)

        return [(item["document"], item["score"]) for item in final_results[:k]]

with open("report.md", "r", encoding="utf-8") as f:
    text = f.read()

chunks = chunk_by_section(text)

retriever = Retriever(
    VectorIndex(),
    BM25Index()
)

for chunk in chunks:
    retriever.add_document({"content": chunk})

query = "What happened with INC-2023-Q4-011?"

results = retriever.search(query, k=3, k_rrf=60)

print("\nHybrid RAG Results:\n")

for doc, score in results:
    print("RRF Score:", score)
    print(doc["content"][:500])
    print("-" * 70)