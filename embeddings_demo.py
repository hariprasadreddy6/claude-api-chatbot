from dotenv import load_dotenv
import voyageai

load_dotenv()

client = voyageai.Client()

def generate_embedding(text):

    result = client.embed(
        [text],
        model="voyage-3-large",
        input_type="document"
    )

    return result.embeddings[0]

text = "Artificial Intelligence is transforming healthcare."

embedding = generate_embedding(text)

print("\n===== EMBEDDING GENERATED =====\n")

print("Embedding Length:", len(embedding))

print("\nFirst 10 Numbers:\n")

print(embedding[:10])