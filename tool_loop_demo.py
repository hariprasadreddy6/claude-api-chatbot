from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolParam
from datetime import datetime
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time. Use this when the user asks for the current date or time.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format string. Example: '%H:%M:%S' for time only.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

tools = [get_current_datetime_schema]

def chat(messages):
    return client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        tools=tools,
        temperature=0.2
    )

def text_from_message(message):
    return "\n".join(
        block.text for block in message.content
        if block.type == "text"
    )

def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def run_tools(message):
    tool_result_blocks = []

    for block in message.content:
        if block.type == "tool_use":
            try:
                tool_output = run_tool(block.name, block.input)

                tool_result_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(tool_output),
                    "is_error": False
                })

            except Exception as e:
                tool_result_blocks.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": f"Error: {e}",
                    "is_error": True
                })

    return tool_result_blocks

def run_conversation(messages):
    while True:
        response = chat(messages)

        messages.append({
            "role": "assistant",
            "content": response.content
        })

        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)

        messages.append({
            "role": "user",
            "content": tool_results
        })

    return messages

messages = [
    {
        "role": "user",
        "content": "What is the exact current time in HH:MM:SS format?"
    }
]

run_conversation(messages)