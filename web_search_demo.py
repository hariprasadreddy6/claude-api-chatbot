from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

web_search_schema = {
    "type": "web_search_20250305",
    "name": "web_search",
    "max_uses": 3
}

messages = [
    {
        "role": "user",
        "content": "What are the latest developments in artificial intelligence today?"
    }
]

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[web_search_schema]
)

print("\n=== FULL RESPONSE ===\n")

for block in response.content:

    print(f"\nBLOCK TYPE: {block.type}\n")

    # normal text
    if block.type == "text":
        print(block.text)

    # search query
    elif block.type == "server_tool_use":
        print("Search Query:")
        print(block.input)

    # search results
    elif block.type == "web_search_tool_result":
        print("Search Results Received")

        for result in block.content:
            if result.type == "web_search_result":
                print("\nTitle:", result.title)
                print("URL:", result.url)