from fastapi import FastAPI
from backend.api.chat import router as chat_router
from backend.api.document import router as doc_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(doc_router)

@app.get("/")
def home():
    return {"status": "running"}