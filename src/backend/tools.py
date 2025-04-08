from langchain_core.tools import tool
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import json


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)  # Directory of tools.py (same as main.py)
# file_path = os.path.join(BASE_DIR, "cleaned_data_3.xlsx")  # Full path to the Excel file
file_path = os.path.join(BASE_DIR, "cleaned_ai_products.xlsx") 

df = pd.read_excel(file_path)
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
#             "fat per 100"

#         ],
#         axis=1,
#         inplace=True,
#     )
# df.to_excel("cleaned_ai_products.xlsx", index=False)


@tool
def initial_data_search(
    query, df=df, threshold=98
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

