from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

athlete_info = """
Height: 180 cm
Weight: 75 kg
Goal: Muscle gain
Dietary restrictions: Vegetarian
"""

prompt = f"""
<athlete_information>
{athlete_info}
</athlete_information>

Generate a 1-day meal plan based on the athlete information above.

Requirements:
- Include breakfast, lunch, dinner, and snacks
- Include calories
- Include protein estimates
"""

response = client.messages.create(
    model=model,
    max_tokens=600,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

print(response.content[0].text)