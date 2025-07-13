from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")

app = FastAPI()

class GenerateRequest(BaseModel):
    query: str
    context: str = ""
    llm: str

@app.post("/generate")

def generate(req: GenerateRequest):
    if req.llm == "gemini":
        prompt = f"""次の質問に文脈を踏まえて回答してください。

質問: {req.query}
文脈: {req.context}
"""
        try:
            response = gemini_model.generate_content(prompt)
            return {"answer": response.text}
        except Exception as e:
            return {"error": str(e)}
        
    # 他のLLM（例: AOAI）に対応する場合はここに追加
    return {"error": "LLM is not supported"}