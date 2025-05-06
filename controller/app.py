from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask(req: AskRequest):
    # Step 1: retrieverに問い合わせ
    retriever_res = requests.post(
        "http://retriever:8001/retrieve",
        json={"query": req.query}
    )
    context = retriever_res.json().get("context", "")

    # Step 2: generator に問い合わせ
    generator_res = requests.post(
        "http://generator:8002/generate",
        json={
            "query": req.query,
            "context": context
        }
    )
    return generator_res.json()