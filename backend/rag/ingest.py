from backend.rag.vectorstore.faiss_store import add_text_chunks


def ingest_document(text: str):

    chunks = text.split(". ")

    add_text_chunks(chunks)

    return {
        "chunks": len(chunks)
    }