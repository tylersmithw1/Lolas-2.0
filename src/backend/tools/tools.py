"These are tools that we 'give' to the AI agents to use in chat_service and recommendation_service."

from langchain_core.tools import tool
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json


# --starts here---this is for dropping columns and creating a new excel file with only the columns the chat service ai agent needs to use
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# file_path = os.path.join(BASE_DIR, "cleaned_data_4.xlsx")
# df = pd.read_excel(file_path)

# df.drop(
#         [
#             "price",
#             "servingspercontainer",
#             "servingsize",
#             "energykcal",
#             "fat",
#             "saturatedfat",
#             "transfat",
#             "carbohydrates",
#             "sugar",
#             "salt",
#             "fibre",
#             "protein",
#             "ingredients",
#             "image",
#             "redmeat",
#             "shelfrank",
#             "packsize",
#             "packunit",
#             "protein per 100",
#             "fibre per 100",
#             "carbohydrates per 100",
#             "transfat per 100",
#             "fat per 100",
#             "nns_flag"

#         ],
#         axis=1,
#         inplace=True,
#     )
# df.to_excel("ai_products_clean.xlsx", index=False)
# ---ends here---

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(
    BASE_DIR, "ai_products_clean.xlsx"
)  # Full path to the ai Excel file
chat_service_df = pd.read_excel(file_path)


@tool  # this decorator is how langchain 'injects' the tools into the AI agent. This tool is used in the chat_service.py file
def initial_data_search(query, df=chat_service_df, threshold=95):
    """Use this tool to retrieve the immediate food data relating to the user's search term."""  # need to add a docstring to the function so the AI agent knows what it does

    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].fillna("").astype(str)

    # columns_to_search = ["aisle", "shelf", "product", "department"]
    columns_to_search = ["product"]

    # Create an empty list to hold the rows that match the query
    matching_rows = []

    # Perform the fuzzy search for each row
    for index, row in df.iterrows():
        row_matches = False
        for column in columns_to_search:
            # Get the value of the current cell
            cell_value = str(row[column])

            # Perform fuzzy matching between the query and the column value
            match_score = fuzz.partial_ratio(query.lower(), cell_value.lower())

            # If the match score is above the threshold, consider it a match
            if match_score >= threshold:
                row_matches = True
                break  # No need to check other columns if one matches

        # If a match is found in any column, append the row to the result
        if row_matches:
            matching_rows.append(row)

    # Convert matching rows to a DataFrame
    filtered_df = pd.DataFrame(matching_rows)

    if filtered_df.empty:
        return json.dumps([])  ## Return an empty JSON array if no matches found

    # return filtered_df
    if not filtered_df.empty:
        result_json = filtered_df.to_dict(orient="records")  # List of dictionaries
        try:
            json_str = json.dumps(result_json)  # Try to serialize the result to JSON
        except TypeError as e:
            print(f"Serialization error: {e}")
            print(f"Problematic row: {matching_rows[0]}")
        return json_str
        # return result_json  # Return the JSON result

    # return []


# #print(initial_data_search.invoke("Ice Mountain Brand 100% Natural Spring Water, 16.9-Ounce Bottles (Pack Of 32)"))

##--starts here---this is for dropping columns and creating a new excel file with only the columns the recommendation ai agent needs to use
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# file_path2 = os.path.join(BASE_DIR, "with_price.xlsx")  #with price is an excel sheet that has all the cleaning PLUS the price per serving column added to it
# it's deleted in this repo, but to find how its made or recreate it, if you go to clean_dataset.py, uncomment 'dc.price_per_container()'
# df2 = pd.read_excel(file_path2)

# df2.drop(
#         [
#             "department",
#             "aisle",
#             "price",
#             "servingspercontainer",
#             "servingsize",
#             "energykcal",
#             "fat",
#             "saturatedfat",
#             "transfat",
#             "carbohydrates",
#             "sugar",
#             "salt",
#             "fibre",
#             "protein",
#             "ingredients",
#             "image",
#             "redmeat",
#             "shelfrank",
#             "packsize",
#             "packunit",
#             "protein per 100",
#             "fibre per 100",
#             "carbohydrates per 100",
#             "transfat per 100",
#             "fat per 100",
#             "high_sugar_flag",
#             "high_sodium_flag",
#             "high_saturated_fat_flag",
#             "high_calories_flag",

#         ],
#         axis=1,
#         inplace=True,
#     )
# df2.to_excel("recs_ai_products.xlsx", index=False)  #for reference, recs_ai_products.xlsx is the same excel as recommendation_products.xlsx in the services folder


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path2 = os.path.join(
    BASE_DIR, "recs_ai_products.xlsx"
)  # Full path to the recs_ai Excel file
recs_service_df = pd.read_excel(file_path2)


@tool  # this decorator is how langchain 'injects' the tools into the AI agent. This tool is used in the recommendation_service.py file
def get_similar_shelf_products(product_name, df=recs_service_df, threshold=50):
    """Use this tool to retrieve similar products from the same shelf."""  # need to add a docstring to the function so the AI agent knows what it does

    # Step 1: Fuzzy match to get closest product name
    product_list = df["product"].tolist()
    match, score = process.extractOne(
        product_name, product_list, scorer=fuzz.token_sort_ratio
    )
    if score < threshold:
        print(f"No close match found for product '{product_name}'.")
        return json.dumps([])

    # Step 2: Get the shelf value for the matched product
    shelf_value = df.loc[df["product"] == match, "shelf"].values[0]
    print(f"Closest product name: {match}, Shelf: {shelf_value}")

    # Step 3: Filter DataFrame by shelf
    matching_rows = df[df["shelf"] == shelf_value]

    # Convert matching rows to a DataFrame
    filtered_df = pd.DataFrame(matching_rows)

    if filtered_df.empty:
        return json.dumps([])  # Return an empty JSON array if no matches found

    # return filtered_df
    if not filtered_df.empty:
        result_json = filtered_df.to_dict(orient="records")  # List of dictionaries
        try:
            json_str = json.dumps(result_json)  # Try to serialize the result to JSON
        except TypeError as e:
            print(f"Serialization error: {e}")
            print(f"Problematic row: {matching_rows[0]}")
        return json_str
