from datetime import datetime
from anthropic.types import ToolParam

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):
    if not date_format:
        raise ValueError("date_format cannot be empty")

    return datetime.now().strftime(date_format)

get_current_datetime_schema = ToolParam({
    "name": "get_current_datetime",
    "description": "Returns the current date and time formatted according to the specified format. Use this tool when the user asks for the current date, current time, or needs time awareness for scheduling. The tool returns a string formatted using Python strftime format codes.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "Python strftime format string. Example: '%Y-%m-%d %H:%M:%S' for full datetime or '%H:%M' for time only.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

print(get_current_datetime())
print(get_current_datetime("%H:%M"))
print(get_current_datetime_schema)