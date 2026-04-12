import os
from fastapi import FastAPI
from pydantic import BaseModel
from  analytics import Inventory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#Load dotenv
load_dotenv()
app=FastAPI() #Creating instance of FASTAPI()
inventory=Inventory("data/my_actual_alseer_portfolio.csv")
client=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                  model_name="gpt-4o-mini",
                  temperature=0)
                  
                  )
class QueryRequest(BaseModel):
      question: str

class QueryResponse(BaseModel):
      answer: str


def classify_intent(question:str):
    #write the prompt     


@app.post("/query") #decorator
def query(request: QueryRequest):
      return QueryResponse(answer=str(inventory.metrics))
                        