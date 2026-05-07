from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolParam
from datetime import datetime

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")

    return datetime.now().strftime(date_format)

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format. Use this when the user asks for current date or time.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format string. Example: '%H:%M:%S' for exact time.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

messages = [
    {
        "role": "user",
        "content": "What is the exact time formatted as HH:MM:SS?"
    }
]

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)

print("Full response content:")
print(response.content)

print("\nMessage blocks:")
for block in response.content:
    print("Block type:", block.type)

    if block.type == "text":
        print("Text:", block.text)

    if block.type == "tool_use":
        print("Tool name:", block.name)
        print("Tool input:", block.input)
        print("Tool ID:", block.id)