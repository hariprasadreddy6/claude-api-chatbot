from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

model = "claude-sonnet-4-6"

# Upload CSV file
uploaded_file = client.beta.files.upload(
    file=open("streaming.csv", "rb")
)

print("Uploaded File ID:", uploaded_file.id)

response = client.messages.create(
    model=model,
    max_tokens=2000,

    messages=[
        {
            "role": "user",

            "content": [
                {
                    "type": "text",

                    "text": (
                        "Analyze this streaming dataset. "
                        "Find major churn patterns and "
                        "give a short business summary."
                    )
                },

                {
                    "type": "container_upload",
                    "file_id": uploaded_file.id
                }
            ]
        }
    ],

    tools=[
        {
            "type": "code_execution_20250522",
            "name": "code_execution"
        }
    ]
)

print("\n===== RESPONSE =====\n")

for block in response.content:

    print("\nBLOCK TYPE:", block.type)

    if block.type == "text":
        print(block.text)

    elif block.type == "server_tool_use":
        print("\nClaude Executed Code:")
        print(block.input)

    elif block.type == "code_execution_tool_result":
        print("\nExecution Result:")
        print(block.content)