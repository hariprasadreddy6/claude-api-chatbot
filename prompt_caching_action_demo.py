from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

long_context = """
You are an expert AI tutor. Explain concepts clearly and simply.
Use beginner-friendly examples. Avoid unnecessary complexity.
""" * 400

def ask_claude(question):
    response = client.messages.create(
        model=model,
        max_tokens=500,
        system=[
            {
                "type": "text",
                "text": long_context,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    print("\n===== RESPONSE =====\n")

    for block in response.content:
        if block.type == "text":
            print(block.text)

    print("\n===== USAGE =====\n")
    print(response.usage)

print("\nFIRST REQUEST")
ask_claude("Explain prompt caching in one paragraph.")

print("\nSECOND REQUEST")
ask_claude("Explain prompt caching in 3 bullet points.")