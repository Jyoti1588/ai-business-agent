from fastapi import APIRouter
from pydantic import BaseModel
import os, json
from google import genai
from dotenv import load_dotenv

from backend.agent.agent_loop import run_agent
from backend.rag.vectorstore.faiss_store import search as rag_search

load_dotenv()

router = APIRouter()


# ----------------------------
# REQUEST MODEL
# ----------------------------
class ChatRequest(BaseModel):
    message: str


# ----------------------------
# CHAT ENDPOINT
# ----------------------------
@router.post("/chat")
def chat(request: ChatRequest):

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    user_message = request.message.lower()

    # ----------------------------
    # RAG CONTEXT (optional)
    # ----------------------------
    rag_keywords = [
        "document", "pdf", "file", "report",
        "what is", "summarize", "explain"
    ]

    rag_context = ""

    if any(k in user_message for k in rag_keywords):
        results = rag_search(user_message)
        rag_context = "\n".join(results)

    # ----------------------------
    # 🔥 STRONG AGENT PROMPT (FIXED)
    # ----------------------------
    prompt = f"""
You are an AI BUSINESS AUTOMATION AGENT.

You MUST decide actions correctly.

AVAILABLE TOOLS:
1. create_ticket → user has issue, problem, laptop not working, bug, complaint
2. send_email → user wants email, notify, inform, send message
3. none → only if no action needed

RULES:
- If user has ANY problem → MUST use create_ticket
- If user mentions email/notify → MUST use send_email
- You CAN return multiple actions
- NEVER return empty actions if issue exists

CONTEXT (if available):
{rag_context}

OUTPUT FORMAT (ONLY JSON):
{{
  "reply": "short helpful response",
  "actions": ["create_ticket"]
}}

User:
{user_message}
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
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        parsed = json.loads(text[start:end])
    except:
        parsed = {
            "reply": text,
            "actions": []
        }

    # ----------------------------
    # AGENT EXECUTION
    # ----------------------------
    final_result = run_agent(parsed, request.message)

    # ----------------------------
    # FINAL RESPONSE
    # ----------------------------
    return {
        "reply": final_result.get("reply", ""),
        "actions": final_result.get("actions", []),
        "tool_result": final_result.get("tool_result", {}),
        "reflection": final_result.get("reflection", {}),
        "final": True
    }