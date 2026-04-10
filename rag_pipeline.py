import os
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_csv_agent

# Connect Groq LLM and load env file
load_dotenv()
client=ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),
                model_name="llama-3.3-70b-versatile")
verbose=os.getenv("VERBOSE","FALSE")=="True"

print("LLM Connected")

# Create the agent this is LangChain function
agent=create_csv_agent(client,
                       "C:/AI Projects/rag-supply-chain/data/my_actual_alseer_portfolio.csv",
                       verbose=verbose,
                       allow_dangerous_code=True,
                       prefix="""You are a Supply Chain analyst. Always answer questions in 
                       plain English. Do not ask to access "code" or "dataframe". Always respond
                       in a structured format."""
                       
                       )

      




