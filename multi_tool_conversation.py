from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolParam
from datetime import datetime, timedelta
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

def add_duration_to_datetime(start_datetime, days=0):
    if not start_datetime:
        raise ValueError("start_datetime cannot be empty")

    dt = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    new_dt = dt + timedelta(days=days)
    return new_dt.strftime("%Y-%m-%d %H:%M:%S")

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time. Use this when the user asks about current time/date or relative dates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format. Default is full datetime.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

add_duration_to_datetime_schema = ToolParam({
    "name": "add_duration_to_datetime",
    "description": "Adds a number of days to a given datetime string and returns the resulting datetime.",
    "input_schema": {
        "type": "object",
        "properties": {
            "start_datetime": {
                "type": "string",
                "description": "Datetime string in format YYYY-MM-DD HH:MM:SS"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to add"
            }
        },
        "required": ["start_datetime", "days"]
    }
})

tools = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema
]

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
        block.text for block in message.content if block.type == "text"
    )

def run_tools(message):
    tool_results = []

    for block in message.content:
        if block.type == "tool_use":
            try:
                if block.name == "get_current_datetime":
                    result = get_current_datetime(**block.input)

                elif block.name == "add_duration_to_datetime":
                    result = add_duration_to_datetime(**block.input)

                else:
                    raise ValueError(f"Unknown tool: {block.name}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                    "is_error": False
                })

            except Exception as e:
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(e),
                    "is_error": True
                })

    return tool_results

def has_tool_use(message):
    return any(block.type == "tool_use" for block in message.content)

def run_conversation(user_question):
    messages = [
        {"role": "user", "content": user_question}
    ]

    while True:
        response = chat(messages)

        messages.append({
            "role": "assistant",
            "content": response.content
        })

        if not has_tool_use(response):
            return response

        tool_results = run_tools(response)

        messages.append({
            "role": "user",
            "content": tool_results
        })

final_response = run_conversation("What day is 103 days from today?")

print(text_from_message(final_response))