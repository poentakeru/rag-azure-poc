import streamlit as st
import requests

st.title("RAG Demo UI")

query = st.text_input("質問を入力してください")

if st.button("送信") and query:
    res = requests.post(
    "http://controller:8004/ask",
    json={"query": query}
    )
    st.subheader("回答:")
    st.write(res.json().get("answer", "No response"))
