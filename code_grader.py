import json
import ast
import re

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(output, test_case):
    expected_type = test_case["expected_type"].lower()

    if expected_type == "json":
        return validate_json(output)

    if expected_type == "python":
        return validate_python(output)

    if expected_type == "regex":
        return validate_regex(output)

    return 0

# quick test
test_cases = [
    {"expected_type": "JSON"},
    {"expected_type": "Python"},
    {"expected_type": "Regex"}
]

outputs = [
    '{"name": "Hari", "role": "AI Engineer"}',
    'def hello():\n    return "hello"',
    r'^[a-z0-9-]{3,63}$'
]

for test_case, output in zip(test_cases, outputs):
    score = grade_syntax(output, test_case)
    print(test_case["expected_type"], "score:", score)