import streamlit as st
import requests
import mimetypes

st.title("RAG Demo UI")

# ✅ モデル選択
llm_options = {
    "Gemini": "gemini",
    "Azure OpenAI": "aoai"
}
selected_llm = st.selectbox(
    "使用するモデルを選択してください",
    options=list(llm_options.keys())
    )


# セクション: ユーザーによるドキュメントアップロード
st.header("📁 ドキュメントアップロード") # h2
uploaded_file = st.file_uploader(
    "対応ファイル形式: PDF, Markdown, テキスト, Word",
    type=["pdf", "md", "txt", "docx"]
    )

if uploaded_file is not None:
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)
    if st.button("アップロード"):
        files = {"file": (
            uploaded_file.name, 
            uploaded_file.getvalue(),
            mime_type or "application/octet-stream")
        }
        response = requests.post(
            "http://ingester:8005/upload",
            files=files
        )

        if response.status_code == 200:
            st.success(f"アップロード成功: {uploaded_file.name}")
        else:
            st.error("アップロードに失敗しました")
st.header("チャットUI")
query = st.text_input("質問を入力してください")

if st.button("送信") and query:
    try:
        res = requests.post(
        "http://controller:8004/ask",
        json={
            "query": query,
            "llm": llm_options[selected_llm]}
        )
        if res.status_code == 200:
            st.success("回答:")
            st.markdown(res.json().get("answer", "（回答なし）"))
        else:
            st.error(f"失敗: {res.text}")
    except Exception as e:
        st.error(f"通信エラー: {str(e)}")