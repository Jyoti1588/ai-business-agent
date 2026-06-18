import uuid
from datetime import datetime

def create_ticket(user_message: str):
    ticket_id = str(uuid.uuid4())[:8]

    ticket = {
        "ticket_id": ticket_id,
        "description": user_message,
        "status": "Open",
        "created_at": str(datetime.now())
    }

    # (later we will save to DB / SharePoint)

    return ticket