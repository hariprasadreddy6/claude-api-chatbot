from dotenv import load_dotenv
from anthropic import Anthropic
import voyageai
import numpy as np

load_dotenv()

anthropic_client = Anthropic()
voyage_client = voyageai.Client()

model = "claude-sonnet-4-6"

chunks = [
    "## Medical Research\nThis year saw significant strides in our understanding of XDR-47, a 'bug' we have not seen before.",
    "## Software Engineering\nThis division dedicated significant effort to studying various infection vectors in our distributed systems."
]

def embed_text(text, input_type):
    result = voyage_client.embed(
        [text],
        model="voyage-3-large",
        input_type=input_type
    )
    return np.array(result.embeddings[0])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 1. Embed document chunks
chunk_embeddings = []

for chunk in chunks:
    embedding = embed_text(chunk, input_type="document")
    chunk_embeddings.append(embedding)

# 2. User question
question = "What did the software engineering department do this year?"

# 3. Embed user question
question_embedding = embed_text(question, input_type="query")

# 4. Find most similar chunk
scores = []

for i, chunk_embedding in enumerate(chunk_embeddings):
    score = cosine_similarity(question_embedding, chunk_embedding)
    scores.append((score, chunks[i]))

scores.sort(reverse=True, key=lambda x: x[0])

best_score, best_chunk = scores[0]

print("\nMost Relevant Chunk:\n")
print(best_chunk)
print("\nSimilarity Score:", best_score)

# 5. Send retrieved chunk to Claude
prompt = f"""
Answer the user's question using only the report context.

<user_question>
{question}
</user_question>

<report_context>
{best_chunk}
</report_context>
"""

response = anthropic_client.messages.create(
    model=model,
    max_tokens=300,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

print("\nClaude Answer:\n")
print(response.content[0].text)