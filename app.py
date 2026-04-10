import streamlit as st
import os
from dotenv import load_dotenv
from rag_pipeline import agent #this has llm inside it

#load env
load_dotenv()

st.title("🏭 MZ Supply Chain Q&A")

# Ask questions
question=st.text_input("Ask questions about inventory data:")

if question:
    with st.spinner("Analyzing..."):
       result=agent.invoke(question)
       st.write(result["output"])

