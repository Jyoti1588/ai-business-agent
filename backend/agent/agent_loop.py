import json

from backend.agent.memory import save_memory
from backend.agent.planner import create_plan
from backend.agent.reflection import reflect
from backend.tools_router import execute_tool
def run_agent(ai_response: dict, user_message: str):
    

    action = ai_response.get("action", "none")
    reply = ai_response.get("reply", "")

    tool_results = {}

    # 🚨 GATE: DO NOT RUN TOOLS for normal chat
    if action == "none":
        return {
            "reply": reply,
            "action": action,
            "tool_result": None,
            "reflection": None,
            "final": True
        }

    # 🧠 PLAN ONLY WHEN ACTION EXISTS
    plan = create_plan(action)

    for step in plan:
        result = execute_tool(step, user_message)
        tool_results[step] = result

    reflection_raw = reflect(user_message, tool_results)

    try:
        reflection = json.loads(reflection_raw)
    except:
        reflection = {"is_correct": True}

    save_memory("default", "last_execution", tool_results)

    return {
        "reply": reply,
        "action": action,
        "tool_result": tool_results,
        "reflection": reflection,
        "final": True
    }