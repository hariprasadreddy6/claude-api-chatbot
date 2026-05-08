from dotenv import load_dotenv
from anthropic import Anthropic
import base64

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

image_path = "images/prop1.png"

with open(image_path, "rb") as f:
    image_data = base64.standard_b64encode(
        f.read()
    ).decode("utf-8")

prompt = """
Analyze this image and provide:
1. What you see
2. Risk level
3. Short explanation
"""

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
)

print(response.content[0].text)