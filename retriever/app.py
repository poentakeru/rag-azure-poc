from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Retriever API is running."}

@app.post("/search")
def search(req: SearchRequest):
    return {
        "query": req.query,
        "results": [
            {"id": 1, "context": "これはダミー結果です"},
            {"id": 2, "context": "あとでFAISSに置き換えます"}
        ]
    }
