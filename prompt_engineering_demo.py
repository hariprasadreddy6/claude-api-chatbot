from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

prompt = """
Create a 1-day vegetarian meal plan for muscle gain.

Include:
- Breakfast
- Lunch
- Dinner
- Snacks
- Calories
- Protein estimate
"""

response = client.messages.create(
    model=model,
    max_tokens=500,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print(response.content[0].text)