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

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    prompt = f"""
You are an AI Business Automation Agent.

Return ONLY valid JSON:

{{
  "reply": "short response",
  "action": "none | create_ticket | send_email | create_ticket_and_email"
}}

User:
{request.message}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # ----------------------------
    # SAFE JSON EXTRACTION
    # ----------------------------
    match = re.search(r"\{.*\}", text, re.DOTALL)

    ai_response = {
        "reply": "",
        "action": "none"
    }

    if match:
        try:
            parsed = json.loads(match.group())

            ai_response["reply"] = parsed.get("reply", "")
            ai_response["action"] = parsed.get("action", "none")

        except:
            ai_response["reply"] = text
            ai_response["action"] = "none"
    else:
        ai_response["reply"] = text
        ai_response["action"] = "none"

    # ----------------------------
    # AGENT LOOP
    # ----------------------------
    final_result = run_agent(ai_response, request.message)

    # ----------------------------
    # FINAL SAFETY RETURN (POWER APPS SAFE)
    # ----------------------------
    return {
        "reply": final_result.get("reply", ""),
        "action": final_result.get("action", "none"),
        "tool_result": final_result.get("tool_result", {}),
        "reflection": final_result.get("reflection", {}),
        "final": True
    }