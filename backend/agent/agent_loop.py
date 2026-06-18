def run_agent(ai_response: dict, user_message: str):
    """
    Core Agent Loop:
    - reads AI decision
    - executes tools
    - returns final structured response
    """

    action = ai_response.get("action", "none")
    reply = ai_response.get("reply", "")

    tool_result = None

    # ----------------------------
    # TOOL 1: CREATE TICKET
    # ----------------------------
    if action == "create_ticket":
        tool_result = create_ticket(user_message)

        return {
            "reply": f"✅ Ticket created successfully.",
            "action": action,
            "tool_result": tool_result,
            "final": True
        }

    # ----------------------------
    # TOOL 2: SEND EMAIL
    # ----------------------------
    elif action == "send_email":
        tool_result = send_email(user_message)

        return {
            "reply": f"📧 Email action triggered successfully.",
            "action": action,
            "tool_result": tool_result,
            "final": True
        }

    # ----------------------------
    # DEFAULT: NORMAL CHAT
    # ----------------------------
    else:
        return {
            "reply": reply,
            "action": "none",
            "tool_result": None,
            "final": True
        }


# ----------------------------
# SIMPLE TOOLS (TEMP VERSION)
# ----------------------------
def create_ticket(message: str):
    return {
        "ticket_id": "TICKET-" + str(abs(hash(message)))[:6],
        "status": "created",
        "description": message
    }


def send_email(message: str):
    return {
        "status": "email_triggered",
        "to": "manager@company.com",
        "message": message
    }