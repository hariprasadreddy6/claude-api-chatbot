from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

system_prompt = """
Return only valid JSON.
Do not include explanation.
Do not include markdown.
Do not use ``` code blocks.
"""

prompt = """
Generate an evaluation dataset for AWS-related coding tasks.

Create exactly 3 JSON objects.
Each object must have:
- task
- expected_type

The expected_type must be one of:
- Python
- JSON
- Regex

Return only a JSON array.
"""

response = client.messages.create(
    model=model,
    max_tokens=500,
    system=system_prompt,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

text = response.content[0].text.strip()

dataset = json.loads(text)

with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Dataset created successfully!")
print(json.dumps(dataset, indent=2))