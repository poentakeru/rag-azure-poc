from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class GenerateRequest(BaseModel):
    query: str
    context: str = ""

@app.post("/generate")
def generate(request: GenerateRequest):
    return {
        "query": request.query,
        "context": request.context,
        "answer": "(これはダミーの回答です)"
    }