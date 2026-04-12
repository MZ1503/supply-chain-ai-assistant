import streamlit as st
import requests


st.title("🏭 MZ Supply Chain AI Assistant")

# Ask questions
question=st.text_input("Ask questions about inventory data:")

if question:
    with st.spinner("Analyzing..."):
       response=requests.post(
           "https://supply-chain-ai-assistant.up.railway.app/query",
            json={"question": question}
       )
       result = response.json()
       st.success(result["answer"])

