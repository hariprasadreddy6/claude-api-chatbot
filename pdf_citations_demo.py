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
    max_tokens=1200,
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
                    },
                    "title": "earth.pdf",
                    "citations": {
                        "enabled": True
                    }
                },
                {
                    "type": "text",
                    "text": "Using citations, explain how Earth formed and what protects Earth from solar wind."
                }
            ]
        }
    ]
)

print("\n===== CLAUDE RESPONSE WITH CITATIONS =====\n")

for block in response.content:
    if block.type == "text":
        print(block.text)

        if hasattr(block, "citations") and block.citations:
            print("\n--- Citations for this text block ---")
            for citation in block.citations:
                print("Document:", citation.document_title)
                print("Pages:", citation.start_page_number, "-", citation.end_page_number)
                print("Cited text:", citation.cited_text[:300])
                print("-" * 50)