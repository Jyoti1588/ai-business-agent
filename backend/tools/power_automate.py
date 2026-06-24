def trigger_flow(message: str):

    return {
        "flow_triggered": True,
        "input": message,
        "status": "success"
    }