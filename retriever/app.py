from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

app = FastAPI()

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dimension = embedding_model.get_sentence_embedding_dimension()
UPLOAD_DIR = "/app/uploads"
INDEX_PATH = os.path.join(UPLOAD_DIR, "index.faiss")
CHUNK_PATH = os.path.join(UPLOAD_DIR, "chunks.json")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 初期化
if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(dimension)

if os.path.exists(CHUNK_PATH):
    with open(CHUNK_PATH) as f:
        chunk_store = {int(k): v for k, v in json.load(f).items()}
else:
    chunk_store = {}

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/")
def root():
    return {"message": "Retriever API is running."}

@app.post("/search")
def search(req: SearchRequest):
    if os.path.exists(INDEX_PATH):
        current_index = faiss.read_index(INDEX_PATH)
    else:
        current_index = index
    if os.path.exists(CHUNK_PATH):
        with open(CHUNK_PATH) as f:
            current_store = {int(k): v for k, v in json.load(f).items()}
    else:
        current_store = chunk_store

    if current_index.ntotal == 0:
        return {"chunks": []}

    query_vec = embedding_model.encode([req.query])
    D, I = current_index.search(np.array(query_vec).astype("float32"), req.top_k)
    chunks = [current_store.get(i, "") for i in I[0]]
    return {"chunks": chunks}

