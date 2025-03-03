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
import json
import re



class GrocerySearch(BaseModel):
    search_string: str


app = FastAPI()

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Directory of tools.py (same as main.py)
file_path = os.path.join(BASE_DIR, "sub-products.xlsx")  # Full path to the Excel file

df = pd.read_excel(file_path)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/grocery")
async def create_ranking(query: GrocerySearch, chat_service: chatService = Depends()):
    try:
        response = chat_service.getChatResponse(query.search_string)
        return response
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/product-info")
async def get_product_info(query: GrocerySearch):
    try:
        # Filter DataFrame based on the search string
        filtered_df = df[
            df["product"].str.contains(query.search_string, case=False, na=False)
        ]

        # Convert filtered DataFrame to a list of dictionaries
        product_list = filtered_df.to_dict(orient="records")

        return {"products": product_list}
    except Exception as e:
        return {"error": str(e)}



@app.post("/grocery-products")
async def create_ranking(query: GrocerySearch, chat_service: chatService = Depends()):
    try:
        response = chat_service.getChatResponse(query.search_string)
        print(f"Raw Chat Response: {response}")  # Debugging output

        # Extract JSON part using regex
        match = re.search(r"<json>\s*(.*?)\s*</json>", response, re.DOTALL)
        if match:
            json_string = match.group(1)  # Extract only the JSON content
        else:
            raise ValueError("Chat response does not contain valid JSON.")

        # Convert extracted JSON string to a Python object
        json_data = json.loads(json_string)

        return JSONResponse(content={"products": json_data})

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))






