from backend.tools.create_ticket import create_ticket
from backend.tools.send_email import send_email
from backend.tools.document_reader import document_reader
from backend.tools.power_automate import trigger_flow
from backend.rag.vectorstore.faiss_store import search as rag_search


def execute_tool(action: str, message: str):

    tools = {
        "create_ticket": create_ticket,
        "send_email": send_email,
        "document_reader": document_reader,
        "power_automate": trigger_flow,
        "rag_search": rag_search
    }

    tool = tools.get(action)

    if not tool:
        return {
            "error": f"Unknown tool: {action}"
        }

    # special case for rag_search (needs query instead of message)
    if action == "rag_search":
        return tool(message)

    return tool(message)