from datetime import datetime

def send_email(message: str):

    return {
        "status": "sent",
        "to": "support@company.com",
        "message": message,
        "sent_at": str(datetime.now())
    }