def create_plan(action: str):

    if action == "create_ticket":
        return ["create_ticket"]

    if action == "send_email":
        return ["send_email"]

    if action == "create_ticket_and_email":
        return [
            "create_ticket",
            "send_email"
        ]

    return []