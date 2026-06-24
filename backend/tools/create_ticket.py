import uuid
from datetime import datetime

def create_ticket(message: str):
    return {
        "ticket_id": str(uuid.uuid4())[:8],
        "description": message,
        "status": "Open",
        "created_at": str(datetime.now())
    }