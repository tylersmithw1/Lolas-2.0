"tool for ai agent to search for food data in a pandas dataframe using fuzzy matching"
from langchain_core.tools import tool
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  
file_path = os.path.join(BASE_DIR, "clean_ai_products.xlsx")  # Full path to the Excel file
search_df = pd.read_excel(file_path)
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
# df.to_excel("clean_ai_products.xlsx", index=False)


@tool
def initial_data_search(
    query, df=search_df, threshold=95
):
    """Use this tool to retrieve the immediate food data relating to the user's search term."""

    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].fillna("").astype(str)

    #columns_to_search = ["aisle", "shelf", "product", "department"]
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
        return json.dumps([]) ## Return an empty JSON array if no matches found

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


#print(initial_data_search.invoke("Ice Mountain Brand 100% Natural Spring Water, 16.9-Ounce Bottles (Pack Of 32)"))

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Directory of tools.py (same as main.py)
file_path2 = os.path.join(BASE_DIR, "rec_products.xlsx")  # Full path to the Excel file
rec_df = pd.read_excel(file_path2)
#print(rec_df.head(5))

@tool
def get_similar_shelf_products(product_name, df=rec_df, threshold=80):
    """Use this tool to retrieve similar products from the same shelf."""

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
    
#print(get_similar_shelf_products.invoke(("Real Good Pepperoni Pizza Snack Bites, 8.5 Oz Box, 8 Count")))
