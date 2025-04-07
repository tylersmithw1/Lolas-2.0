# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from service import chatService
from fastapi import FastAPI, HTTPException, Depends
import os
from fastapi.responses import JSONResponse
import pandas as pd
import logging





class GrocerySearch(BaseModel):
    search_string: str


app = FastAPI()

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Directory of tools.py (same as main.py)
#file_path = os.path.join(BASE_DIR, "sub-products.xlsx")  # Full path to the Excel file
file_path = os.path.join(BASE_DIR, "cleaned_data.xlsx") 

df = pd.read_excel(file_path)

origins = ["http://localhost:8000",  # React default port
    "http://127.0.0.1:8000",
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:5173", 
    "http://localhost:5174", 
    "http://127.0.0.1:5174"
    
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.post("/grocery")
async def create_ranking(query: GrocerySearch, chat_service: chatService = Depends()):
    try:
        response = chat_service.getChatResponse(query.search_string)
        logger.info(f"Chatbot raw response: {response}")
        
    
        ranked_names = response.get("ranking", [])
        # Match and return full product details from your Excel df
        matched = df[df["product"].isin(ranked_names)]

        # Keep the original ranking order
        ranked_detailed = []
        for name in ranked_names:
            product_row = matched[matched["product"] == name]
            if not product_row.empty:
                ranked_detailed.append(product_row.iloc[0].to_dict())

        return {"products": ranked_detailed}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))