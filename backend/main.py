from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from google import genai
from backend.agent.agent_loop import run_agent
import json
import re

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

app = FastAPI()


# ----------------------------
# Request Model
# ----------------------------
class ChatRequest(BaseModel):
    message: str


# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def home():
    return {"status": "running"}


# ----------------------------
# AI Chat Endpoint (AGENT READY)
# ----------------------------
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        prompt = f"""
You are an AI Business Agent.

Return ONLY valid JSON.

Format:
{{
  "reply": "string",
  "action": "none | create_ticket | send_email"
}}

User message:
{request.message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # extract JSON safely
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            ai_response = json.loads(match.group())
        else:
            ai_response = {
                "reply": text,
                "action": "none"
            }

        # 🔥 THIS IS THE KEY FIX (Agent Loop is used here)
        final_result = run_agent(ai_response, request.message)

        return final_result

    except Exception as e:
        return {
            "reply": f"AI error: {str(e)}",
            "action": "none"
        }