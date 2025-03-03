# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from service import chatService
from fastapi import FastAPI, HTTPException, Depends
import os
import pandas as pd


class GrocerySearch(BaseModel):
    search_string: str


app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of tools.py (same as main.py)
file_path = os.path.join(BASE_DIR, "sub-products.xlsx") # Full path to the Excel file

df = pd.read_excel(file_path)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/grocery")
async def create_ranking(query: GrocerySearch, chat_service: chatService = Depends()):
    try:
        response = chat_service.getChatResponse(query.search_string)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


