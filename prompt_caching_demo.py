from dotenv import load_dotenv
from anthropic import Anthropic
import base64

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

pdf_path = "sample.pdf"

with open(pdf_path, "rb") as f:
    pdf_data = base64.standard_b64encode(
        f.read()
    ).decode("utf-8")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data
                },
                "title": "sample.pdf",
                "citations": {
                    "enabled": True
                }
            },
            {
                "type": "text",
                "text": "Summarize this PDF in 5 bullet points."
            }
        ]
    }
]

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages
)

print("\n===== FIRST RESPONSE =====\n")

print(response.content[0].text)

# Follow-up question using same document context

messages.append({
    "role": "assistant",
    "content": response.content
})

messages.append({
    "role": "user",
    "content": "What are the most important topics discussed in this document?"
})

response2 = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages
)

print("\n===== SECOND RESPONSE =====\n")

print(response2.content[0].text)