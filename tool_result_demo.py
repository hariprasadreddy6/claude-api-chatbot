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

# 1. Claude asks to use tool
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)

# 2. Save Claude's assistant message with tool_use block
messages.append({
    "role": "assistant",
    "content": response.content
})

# 3. Find tool_use block and run function
tool_results = []

for block in response.content:
    if block.type == "tool_use":
        if block.name == "get_current_datetime":
            try:
                result = get_current_datetime(**block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                    "is_error": False
                })

            except Exception as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(e),
                    "is_error": True
                })

# 4. Send tool result back to Claude
messages.append({
    "role": "user",
    "content": tool_results
})

final_response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_datetime_schema]
)

# 5. Print final answer
print(final_response.content[0].text)