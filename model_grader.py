from dotenv import load_dotenv
from anthropic import Anthropic
import json
from statistics import mean

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

def call_claude(messages, system=None, max_tokens=800, temperature=0.3):
    params = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": temperature
    }

    if system:
        params["system"] = system

    response = client.messages.create(**params)
    return response.content[0].text.strip()

def run_prompt(test_case):
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    messages = [{"role": "user", "content": prompt}]
    return call_claude(messages)

def grade_by_model(test_case, output):
    system_prompt = """
You are an expert code reviewer.
Return only valid JSON.
Do not include markdown.
Do not include explanation outside JSON.
"""

    eval_prompt = f"""
Evaluate this AI-generated solution.

Task:
{test_case["task"]}

Expected output type:
{test_case["expected_type"]}

Solution:
{output}

Return JSON with:
- strengths: array of 1-3 strengths
- weaknesses: array of 1-3 weaknesses
- reasoning: short explanation
- score: number from 1 to 10
"""

    messages = [{"role": "user", "content": eval_prompt}]
    text = call_claude(messages, system=system_prompt, max_tokens=500, temperature=0.0)

    return json.loads(text)

def run_test_case(test_case):
    output = run_prompt(test_case)
    grade = grade_by_model(test_case, output)

    return {
        "test_case": test_case,
        "output": output,
        "score": grade["score"],
        "reasoning": grade["reasoning"],
        "strengths": grade["strengths"],
        "weaknesses": grade["weaknesses"]
    }

def run_eval(dataset):
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])

    return results, average_score

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results, average_score = run_eval(dataset)

with open("graded_results.json", "w") as f:
    json.dump(
        {
            "average_score": average_score,
            "results": results
        },
        f,
        indent=2
    )

print("Model grading completed!")
print("Average score:", average_score)
print(json.dumps(results, indent=2))