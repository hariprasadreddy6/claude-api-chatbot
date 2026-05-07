from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

prompt = """
Generate a 1-day vegetarian meal plan for muscle gain.

Requirements:
1. Include breakfast, lunch, dinner, and snacks
2. Show calories for each meal
3. Include protein, carbs, and fats
4. Mention meal timing
5. Keep calories around 2500
6. Use affordable foods

Steps:
1. Estimate calorie needs
2. Select high-protein foods
3. Balance carbs and fats
4. Create meal timing schedule
"""

response = client.messages.create(
    model=model,
    max_tokens=700,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print(response.content[0].text)