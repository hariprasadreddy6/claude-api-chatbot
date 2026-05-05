from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

system_prompt = """
You are a helpful AI assistant.
Answer clearly and creatively when needed.
"""

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model=model,
        max_tokens=200,
        messages=messages,
        system=system_prompt,
        temperature=1.0
    )

    reply = response.content[0].text
    print("Claude:", reply)

    messages.append({"role": "assistant", "content": reply})