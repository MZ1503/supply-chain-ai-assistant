<<<<<<< HEAD
# MZ Supply Chain Q&A
A natural language query engine that answers in plain English about the inventory data.
=======
 MZ Supply Chain RAG Q&A System (Need to Fine-Tune)
>>>>>>> baec2ae463358934e4f9b49ad12f07021fcded51

#Description:
This bot can help in answering questions about your inventory data in a natural language which automates the manual excel based calculation. Its useful for higher management or managers who wants quick answers and an overview about the inventory.

<<<<<<< HEAD
# Tech Tools
- LangChain Pandas Agent 
- Groq LLaMA-3 70B
=======
Ask questions like:
- "Which brand has most expired products?"
- "Which products are expiring soon?"

## Tech Stack
- Python
- LangChain
- Groq LLM (Llama 3)
- ChromaDB
- HuggingFace Embeddings
>>>>>>> baec2ae463358934e4f9b49ad12f07021fcded51
- Streamlit
- Python

# Architecture
Initially, I built this bot using RAG. However, I realized that RAG uses semantic similiarity search which cannot do aggregatios, count and calculations. Therefore I used Pandas Agent for a structured and calculated output.

# Installation
1. Clone the repo
2. Install dependencies: pip install -r requirements.txt
3. Add your API keys to .env
4. Run: streamlit run app.py

<<<<<<< HEAD
## Questions I have tested on
1. Which brands have the most expired products?
2. How many products are expired?
3. How many rows are in the inventory?  
=======
## Here's the link to the app:
https://rag-supply-chain-mariyam.streamlit.app
>>>>>>> baec2ae463358934e4f9b49ad12f07021fcded51
