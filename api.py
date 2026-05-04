import os
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from  analytics import Inventory
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

#Load dotenv
load_dotenv()
app=FastAPI() #Creating instance of FASTAPI()
@app.get("/health")
def health():
    return {"status": "healthy"}
inventory=Inventory("data/my_actual_alseer_portfolio.csv")
client=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                  model="gpt-4o-mini",
                  temperature=0)
                  
                  
class QueryRequest(BaseModel):
      question: str

class QueryResponse(BaseModel):
      answer: str


def classify_intent(question:str) -> str:
    #write the prompt     
    prompt=f"""You are a supply chain analytics assistant.

Given this question: "{question}"

Reply with ONLY one metric name from this list, nothing else:
expired_count, expiring_7_days, top_expired_brand, 
top_revenue_brand, total_inv_val, highest_stock_category,
products_zero_stock, expiry_rate_brand, urgent_brands, top_10_products"""
    
    response=client.invoke(prompt)
    return response.content.strip()


def format_answer(metric_key:str, metrics: dict) -> str:
    answers={
         "expired_count":f"There are {metrics['expired_count']} expired products.",
         "expiring_7_days":f"The products expiring in 7 days are {len(metrics['expiring_7_days'])}.",
         "top_expired_brand":f"The top expiring brand is {metrics['top_expired_brand']}",
         "top_revenue_brand":f"The top revenue brand is {metrics['top_revenue_brand']}",
        "total_inv_val":f"The total inventory value is {metrics['total_inv_val']}.",
        "highest_stock_category":f"The {metrics['highest_stock_category']} category has the highest stock.",
        "products_zero_stock":f"There are {len(metrics['products_zero_stock'])} products with zero stock.",
        "expiry_rate_brand":f"Expiry rates by brand: {metrics['expiry_rate_brand']}.",
        "urgent_brands": f"Brands needing urgent attention: {','.join(metrics['urgent_brands'])}.",
        "top_10_products": ",".join([f"{p['BRAND']} ({p['CATEGORY']}): AED {p['REVENUE']:,.0f}"for p in metrics['top_10_products']])
    }

    return answers.get(metric_key,"I didn't quite understand! Shall we try again?")

@app.post("/query") #decorator
def query(request: QueryRequest):
    try:
        if not request.question.strip():
            raise ValueError("Question cannot be empty")
        
        metric_key=classify_intent(request.question)
        answer=format_answer(metric_key,inventory.metrics)
        return QueryResponse(answer=answer)
    except ValueError as e:
         raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something went wrong")



