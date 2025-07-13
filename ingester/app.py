from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import fitz # PyMuPDF
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import uuid

app = FastAPI()

# モデルとインデックスの初期化、ハイパーパラメータ
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
    )
dimension = embedding_model.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
default_max_length = 300
default_top_k = 3
chunk_store = {}


# チャンク分割（目安: 300文字）
def split_into_chunks(text: str, max_length=default_max_length):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# PDF -> テキスト抽出（PyMuPDF使用）
def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    all_text = ""
    for page in doc:
        all_text += page.get_text() + "\n"
    return all_text

# Markdown変換（今回はシンプルに扱います）
def to_markdown(text):
    return f"```\n{text.strip()}```"


UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".md", ".txt", ".docx"}



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    _, ext = os.path.splitext(file.filename)

    if ext.lower() not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content={"error": f"このファイル形式は許可されていません: {ext}"}
        )
    
    ## 現状pdfのみの取り扱いなので、暫定的に以下のようにエラーハンドリングする
    if ext.lower() != ".pdf":
        return JSONResponse(
            status_code=400,
            content={"error": f"{ext}形式の文書は現在サポートされていません。PDFのみ対応しています。"}
        )
    
    save_path = os.path.join(UPLOAD_DIR, file.filename)
   
    try:
        # ========================
        # 1. Markdownへの変換
        # ========================
        # 1.1. pdfファイル場合の処理
        # ========================
        if ext.lower() == ".pdf":
            try:
                file_bytes = await file.read()
                raw_text = extract_text_from_pdf(file_bytes)
                md_text = to_markdown(raw_text)
                with open(save_path.replace(".pdf", ".md"), "w") as f:
                    f.write(md_text)
                chunks = split_into_chunks(raw_text)
            except Exception as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"pdf文書をマークダウンに変換する処理に失敗しました。"}
        )
        # =========================
        # 2. embedding
        # =========================
        # 2.1. "sentence-transformers/all-MiniLM-L6-v2"によるエンべディング
        # """
        # 現状は、"sentence-transformers/all-MiniLM-L6-v2"で固定です。
        # エンべディングモデルを選択できるようにするには、UIと合わせて改修が必要
        # """
        # ==========================
        embeddings = embedding_model.encode(chunks, normalize_embeddings=True)
        embeddings = np.array(embeddings).astype("float32")
        
        # ==========================
        # 3. ベクトルデータベース化
        # ==========================
        # 3.1. FAISSの場合
        # """
        # 現状は、FAISSのみです。
        # ベクトルデータベース化の様態を選択できるようにするには、UIと合わせての改修が必要
        # """
        # ===========================
        # FAISSへ登録
        start_id = index.ntotal  # 追加前の件数を取得
        index.add(embeddings)
        for i, chunk in enumerate(chunks):
            chunk_store[start_id + i] = chunk

        return JSONResponse({
            "message": "アップロード・登録完了", 
            "chunks": len(chunks)
            })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

@app.get("/search")
def search(query: str, top_k: int = default_top_k):
    try:
        query_vec = embedding_model.encode([query])
        D, I = index.search(query_vec, top_k)
        results = [
            chunk_store.get(i, "不明") for i in I[0]
        ]
        return {"query": query, "results": results}
    except Exception as e:
        return JSONResponse(
            {"error": str(e)}, status_code=500
        )