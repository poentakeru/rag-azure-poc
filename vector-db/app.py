from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# チャンクベクトルの登録用リクエストスキーマ
class Chunk(BaseModel):
    id: str
    text: str
    embedding: List[float]

@app.post("/insert")
def insert_chunk(chunk: Chunk):
    # 本来はFAISSなどに保存する処理が入る
    print(f"Received chunk: {chunk.id}")
    return {"status": "ok", "id": chunk.id}
