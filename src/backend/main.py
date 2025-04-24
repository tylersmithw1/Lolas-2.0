"api endpoint for lola's 2.0"
# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
#from src.backend.services.chat_service import chatService
from services.chat_service import chatService
from fastapi import FastAPI, HTTPException, Depends
import os
from fastapi.responses import JSONResponse
import pandas as pd
import logging
from models.grocery_search import GrocerySearch
from models.recommendation import Recommendation
from models.product_name import ProductName
from services.recommendation_service import RecommendationService


app = FastAPI()

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


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  
file_path = os.path.join(BASE_DIR, "cleaned_data_3.xlsx")  #Full path to the Excel file
df = pd.read_excel(file_path)


@app.post("/grocery")
async def create_ranking(query: GrocerySearch, chat_service: chatService = Depends()):
    try:
        response = chat_service.getChatResponse(query.search_string)
       #logger.info(f"Chatbot raw response: {response}")
        print(f"Chatbot raw response: {response}")
        
    
        ranked_names = response.get("ranking", [])
        print(f"ranked names: {ranked_names}")
        # Match and return full product details from your Excel df
        matched = df[df["product"].isin(ranked_names)]
        print(f"matched products: {matched}")

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


@app.post("/recommendations")
async def get_recommendations(query: Recommendation, rec_service: RecommendationService = Depends()):
    try:
        product_name = query.product_name
        column_name = query.column_name
        print(f"product name: {product_name}")
        print(f"column name: {column_name}")

        column_map = {
        "sugar": "sugar per 100",
        "calories": "energykcal per 100",
        "saturated fat": "saturatedfat per 100",
        "sodium": "salt per 100",
        "ultraprocessed": "ultra_processed_flag",
        "nns": "nns_flag"}

        if column_name not in column_map:
            raise HTTPException(status_code=400, detail=f"Invalid column name: {column_name}")

        column_name = column_map[column_name]
        
        response = rec_service.recomendations_by_column(product_name, column_name)

        ranked_names = response.get("ranking", [])
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


@app.post("/ai-recommendations")
async def get_ai_recommendations(query: ProductName, rec_service: RecommendationService = Depends()):
    try:
        response = rec_service.getRecommendationResponse(query.full_product_name)
       #logger.info(f"Chatbot raw response: {response}")
        print(f"Chatbot raw response: {response}")
        
    
        ranked_names = response.get("ranking", [])
        print(f"ranked names: {ranked_names}")
        # Match and return full product details from your Excel df
        matched = df[df["product"].isin(ranked_names)]
        print(f"matched products: {matched}")

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