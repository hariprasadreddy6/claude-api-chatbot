from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import ToolParam
from datetime import datetime, timedelta
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

reminders = []

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")
    return datetime.now().strftime(date_format)

def add_duration_to_datetime(start_datetime, days=0):
    if not start_datetime:
        raise ValueError("start_datetime cannot be empty")

    dt = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    result = dt + timedelta(days=days)
    return result.strftime("%Y-%m-%d %H:%M:%S")

def set_reminder(reminder_text, reminder_datetime):
    if not reminder_text:
        raise ValueError("reminder_text cannot be empty")
    if not reminder_datetime:
        raise ValueError("reminder_datetime cannot be empty")

    reminder = {
        "reminder_text": reminder_text,
        "reminder_datetime": reminder_datetime
    }

    reminders.append(reminder)

    with open("reminders.json", "w") as f:
        json.dump(reminders, f, indent=2)

    return {
        "status": "success",
        "message": "Reminder set successfully",
        "reminder": reminder
    }

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time. Use this when the user asks about current time/date or relative dates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format string.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

add_duration_to_datetime_schema = ToolParam({
    "name": "add_duration_to_datetime",
    "description": "Adds a number of days to a datetime string and returns the result.",
    "input_schema": {
        "type": "object",
        "properties": {
            "start_datetime": {
                "type": "string",
                "description": "Datetime in format YYYY-MM-DD HH:MM:SS"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to add"
            }
        },
        "required": ["start_datetime", "days"]
    }
})

set_reminder_schema = ToolParam({
    "name": "set_reminder",
    "description": "Sets a reminder for a specific datetime and saves it.",
    "input_schema": {
        "type": "object",
        "properties": {
            "reminder_text": {
                "type": "string",
                "description": "The reminder message"
            },
            "reminder_datetime": {
                "type": "string",
                "description": "Reminder datetime in format YYYY-MM-DD HH:MM:SS"
            }
        },
        "required": ["reminder_text", "reminder_datetime"]
    }
})

tools = [
    get_current_datetime_schema,
    add_duration_to_datetime_schema,
    set_reminder_schema
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
        block.text for block in message.content
        if block.type == "text"
    )

def run_tool(tool_name, tool_input):
    if tool_name == "get_current_datetime":
        return get_current_datetime(**tool_input)
    elif tool_name == "add_duration_to_datetime":
        return add_duration_to_datetime(**tool_input)
    elif tool_name == "set_reminder":
        return set_reminder(**tool_input)
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

        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)

        messages.append({
            "role": "user",
            "content": tool_results
        })

    return messages

run_conversation(
    "Set a reminder for my doctor's appointment. It is 177 days after Jan 1st, 2050."
)