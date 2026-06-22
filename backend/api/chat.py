from fastapi import APIRouter
from pydantic import BaseModel
import os, json, re
from google import genai
from backend.agent.agent_loop import run_agent
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


# ----------------------------
# Request Model
# ----------------------------
class ChatRequest(BaseModel):
    message: str


# ----------------------------
# CHAT ENDPOINT
# ----------------------------
@router.post("/chat")
def chat(request: ChatRequest):

    # Create Gemini client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # ----------------------------
    # PROMPT (IMPORTANT PART)
    # ----------------------------
    prompt = f"""
You are an AI Business Automation Agent.

Return ONLY valid JSON.

You can choose:

- none
- create_ticket
- send_email
- create_ticket_and_email

RULE:
If user needs multiple actions → use create_ticket_and_email

Format:
{{
  "reply": "short response",
  "action": "none | create_ticket | send_email | create_ticket_and_email"
}}

User:
{request.message}
"""

    # ----------------------------
    # CALL GEMINI
    # ----------------------------
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # ----------------------------
    # SAFE JSON PARSING
    # ----------------------------
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            ai_response = json.loads(match.group())
        except:
            ai_response = {
                "reply": text,
                "action": "none"
            }
    else:
        ai_response = {
            "reply": text,
            "action": "none"
        }

    # ----------------------------
    # SEND TO AGENT LOOP
    # ----------------------------
    final_result = run_agent(ai_response, request.message)

    return final_result