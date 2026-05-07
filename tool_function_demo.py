from datetime import datetime

def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S"):

    if not date_format:
        raise ValueError("date_format cannot be empty")

    return datetime.now().strftime(date_format)

# default format
print(get_current_datetime())

# only time
print(get_current_datetime("%H:%M"))

# only date
print(get_current_datetime("%Y-%m-%d"))