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

response = client.messages.create(
    model=model,
    max_tokens=1000,

    system=[
        {
            "type": "text",
            "text": (
                "You are an expert PDF analyst. "
                "Answer clearly using the document."
            ),

            # CACHE BREAKPOINT
            "cache_control": {
                "type": "ephemeral"
            }
        }
    ],

    messages=[
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
                    "text": (
                        "Summarize this PDF "
                        "in 5 bullet points."
                    )
                }
            ]
        }
    ]
)

print("\n===== RESPONSE =====\n")

print(response.content[0].text)

print("\n===== USAGE INFO =====\n")

print(response.usage)