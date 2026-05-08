from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

messages = [
    {
        "role": "user",
        "content": "Solve carefully: A store sells apples at 3 for $2. If I buy 18 apples, how much do I pay?"
    }
]

response = client.messages.create(
    model=model,
    max_tokens=2000,
    messages=messages,
    thinking={
        "type": "enabled",
        "budget_tokens": 1024
    }
)

print("\n===== RESPONSE BLOCKS =====\n")

for block in response.content:
    print("Block Type:", block.type)

    if block.type == "thinking":
        print("\nThinking block received")

    elif block.type == "redacted_thinking":
        print("\nRedacted thinking block received")

    elif block.type == "text":
        print("\nFinal Answer:\n")
        print(block.text)