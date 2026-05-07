from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

# fake weather tool
def get_weather(city):
    fake_weather_data = {
        "San Francisco": "72°F and sunny",
        "New York": "65°F and cloudy",
        "St. Louis": "80°F and clear"
    }

    return fake_weather_data.get(city, "Weather data not found")

city = "San Francisco"

weather = get_weather(city)

prompt = f"""
<weather_data>
City: {city}
Current weather: {weather}
</weather_data>

Answer the user's question using the weather data above.

User question:
What's the weather in San Francisco?
"""

response = client.messages.create(
    model=model,
    max_tokens=200,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response.content[0].text)