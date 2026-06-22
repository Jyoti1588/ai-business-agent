from backend.tools.ticket_creator import create_ticket
from backend.tools.email_reader import send_email

def execute_tool(action: str, message: str):

    if action == "create_ticket":
        return create_ticket(message)

    if action == "send_email":
        return send_email(message)

    return None