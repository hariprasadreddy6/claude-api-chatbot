from dotenv import load_dotenv
from anthropic import Anthropic
from statistics import mean
import json

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def call_claude(prompt):
    response = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.content[0].text.strip()

def run_prompt(test_case):
    prompt = f"""
Please solve this task:

{test_case["task"]}
"""

    return call_claude(prompt)

def grade_output(output):
    # simple grading logic
    if len(output) > 50:
        return 8
    else:
        return 5

def run_eval(dataset):
    results = []

    for test_case in dataset:
        output = run_prompt(test_case)

        score = grade_output(output)

        results.append({
            "task": test_case["task"],
            "output": output,
            "score": score
        })

    average_score = mean([r["score"] for r in results])

    return results, average_score

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results, average_score = run_eval(dataset)

print("\nEvaluation Results:\n")
print(json.dumps(results, indent=2))

print("\nAverage Score:", average_score)

with open("average_eval_results.json", "w") as f:
    json.dump({
        "average_score": average_score,
        "results": results
    }, f, indent=2)