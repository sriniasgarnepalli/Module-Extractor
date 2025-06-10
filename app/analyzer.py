import os
import json
import time
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_text_into_chunks(text, max_tokens=2000):
    enc = tiktoken.encoding_for_model("gpt-4o")
    tokens = enc.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [enc.decode(chunk) for chunk in chunks]

def gpt_infer_structure(text_blob):

    prompt = f"""
Given the following documentation content, identify major modules and their submodules. 
For each submodule, generate:
- A clear, helpful description
- A confidence score from 0 to 1 (based on clarity, coverage, and relevance)

Respond only with valid JSON in this format:

[
  {{
    "module": "Module Name",
    "Description": "Description of the module",
    "Confidence": 0.92,
    "Submodules": {{
      "Submodule Name": {{
        "description": "Submodule description",
        "confidence": 0.85
      }}
    }}
  }}
]

Documentation Content:
{text_blob}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content

        # Remove markdown wrapping if present
        content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip(), flags=re.DOTALL)
        return json.loads(content)
    except Exception as e:
        print("GPT error:", e)
        return [{"module": "Error", "Description": str(e), "Submodules": {}}]