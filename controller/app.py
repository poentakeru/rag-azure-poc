from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class AskRequest(BaseModel):
    query: str
    llm: str

@app.post("/ask")
def ask(req: AskRequest):
    # Step 1: retrieverに問い合わせ
    res = requests.post(
        "http://retriever:8001/search",
        json={"query": req.query}
    )
    chunks = res.json().get("chunks", [])
    context = "\n".join(chunks)

    # Step 2: generator に問い合わせ
    generator_res = requests.post(
        "http://generator:8002/generate",
        json={
            "query": req.query,
            "context": context,
            "llm": req.llm
        }
    )
    return generator_res.json()
