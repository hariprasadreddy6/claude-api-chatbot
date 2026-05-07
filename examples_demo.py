from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"

prompt = """
<example>
<sample_input>
Tweet: "Great game tonight!"
</sample_input>

<ideal_output>
Positive
</ideal_output>
</example>

<example>
<sample_input>
Tweet: "Oh great, another flight delay. Amazing."
</sample_input>

<ideal_output>
Negative
</ideal_output>
</example>

Classify this tweet:

Tweet: "I just love when my phone battery dies in 5 minutes."
"""

response = client.messages.create(
    model=model,
    max_tokens=50,
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.2
)

print(response.content[0].text)