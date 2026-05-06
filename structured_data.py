from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

system_prompt = """
Return only valid JSON.
Do not include markdown.
Do not include explanation.
Do not use ``` code blocks.
"""

response = client.messages.create(
    model=model,
    max_tokens=200,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": "Generate a simple student JSON object with name, age, course, and grade."
        }
    ],
    temperature=0.0
)

print(response.content[0].text.strip())