from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def chat(messages):
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=messages,
        temperature=0.3
    )
    return response.content[0].text

def run_prompt(test_case):
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    messages = [
        {"role": "user", "content": prompt}
    ]
    output = chat(messages)
    return output

def run_test_case(test_case):
    output = run_prompt(test_case)

    score = 10  # temporary score, grader will come later

    return {
        "test_case": test_case,
        "output": output,
        "score": score
    }

def run_eval(dataset):
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    return results

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)

with open("eval_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Evaluation completed successfully!")
print(json.dumps(results, indent=2))