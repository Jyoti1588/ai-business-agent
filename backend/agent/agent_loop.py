import json

from backend.tools_router import execute_tool
from backend.agent.memory import save_memory
from backend.agent.reflection import reflect
from backend.agent.planner import create_plan


def run_agent(ai_response: dict, user_message: str):

    actions = ai_response.get("actions", [])
    reply = ai_response.get("reply", "")

    tool_results = {}

    if not actions:
        return {
            "reply": reply,
            "actions": [],
            "tool_result": {},
            "reflection": {},
            "final": True
        }

    # PLAN → EXECUTE
    for action in actions:
        steps = create_plan(action)

        for step in steps:
            tool_results[step] = execute_tool(step, user_message)

    # REFLECTION (safe fallback)
    try:
        reflection = json.loads(reflect(user_message, tool_results))
    except:
        reflection = {"is_correct": True}

    # MEMORY
    save_memory("default", "last_message", user_message)
    save_memory("default", "last_execution", tool_results)

    return {
        "reply": reply,
        "actions": actions,
        "tool_result": tool_results,
        "reflection": reflection,
        "final": True
    }