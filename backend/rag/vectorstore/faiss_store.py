import faiss
import numpy as np
from backend.rag.embeddings import get_embedding

DIM = 384

index = faiss.IndexFlatL2(DIM)
docs = []


def add_text_chunks(chunks):
    global docs

    vectors = [get_embedding(c) for c in chunks]

    index.add(np.array(vectors).astype("float32"))
    docs.extend(chunks)


def search(query, top_k=3):

    qv = np.array([get_embedding(query)]).astype("float32")

    _, idx = index.search(qv, top_k)

    return [docs[i] for i in idx[0] if i < len(docs)]