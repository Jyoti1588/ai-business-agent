from google import genai
import os

def reflect(user_message: str, tool_result: dict):

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
You are a Reflection Agent.

Check if the tool execution is correct.

User request:
{user_message}

Tool result:
{tool_result}

Return ONLY JSON:
{{
  "is_correct": true/false,
  "feedback": "short reason",
  "improvement": "optional suggestion"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text