from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import agent


app=FastAPI() #Creating instance of FASTAPI()

class QueryRequest(BaseModel):
      question: str

class QueryResponse(BaseModel):
      answer: str

@app.post("/query") #decorator
def query(request: QueryRequest):
      result=agent.invoke(request.question)
      return QueryResponse(answer=result["output"])
                        