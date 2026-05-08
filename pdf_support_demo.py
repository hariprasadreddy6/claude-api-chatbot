from dotenv import load_dotenv
from anthropic import Anthropic
import base64

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

pdf_path = "sample.pdf"

with open(pdf_path, "rb") as f:
    file_data = base64.standard_b64encode(
        f.read()
    ).decode("utf-8")

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": file_data
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize this PDF in 5 bullet points."
                }
            ]
        }
    ]
)

print("\n===== PDF SUMMARY =====\n")

print(response.content[0].text)