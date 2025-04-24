"""Recommendation Service Layer."""


import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz, process


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of tools.py (same as main.py)
file_path = os.path.join(BASE_DIR, "recommendation_products.xlsx")  # Full path to the Excel file

DF = pd.read_excel(file_path)
# DF.drop(["department", "aisle", "price", "servingspercontainer", "servingsize", "energykcal", "fat", "saturatedfat", "transfat", "carbohydrates", "sugar", "salt", "fibre", "protein", "ingredients", "redmeat", "shelfrank", "packsize", "packunit", "image", "fat per 100", "transfat per 100", "carbohydrates per 100", "fibre per 100", "protein per 100", "high_sugar_flag", "high_sodium_flag", "high_saturated_fat_flag", "high_calories_flag", ], axis=1, inplace=True)
# DF.to_excel("recommendation_products.xlsx", index=False)


#products repeat in the dataset, sometimes appearing in different shelves. Here we use the first instance of the product's shelf name. so ultimately, need to find and drop duplicates
class RecommendationService:
    """Recommendation class."""
    def __init__(self):
        pass

    def get_closest_product_name(self, product_name, df, threshold=80):
        product_list = df["product"].tolist()
        match, score, idx = process.extractOne(
            product_name, product_list, scorer=fuzz.token_sort_ratio
        )
        if score >= threshold:
            return match
        return None

    def recomendations_by_column(self, product_name, column_name):
        closest_name = self.get_closest_product_name(product_name, DF)
        if not closest_name:
            print(f"No close match found for product '{product_name}'.")
            return None

        shelf_value = DF.loc[DF["product"] == closest_name, "shelf"].values[0]
        print(f"Closest product name: {closest_name}, Shelf: {shelf_value}")

        filtered_df = DF[DF["shelf"] == shelf_value].copy()

        names = filtered_df["product"].tolist()
        vectorizer = TfidfVectorizer().fit([closest_name] + names)
        vectors = vectorizer.transform([closest_name] + names)

        ref_vector = vectors[0]
        other_vectors = vectors[1:]

        similarities = cosine_similarity(ref_vector, other_vectors).flatten()
        filtered_df["name_similarity"] = similarities

        # Keep only those with sufficient similarity
        name_filtered_df = filtered_df[filtered_df["name_similarity"] >= 0.1]

        ref_price = DF[
            (DF["product"].str.lower() == closest_name.lower()) &
            (DF["shelf"].str.lower() == shelf_value.lower())
        ]["price_per_serving"]

        if ref_price.empty:
            print(f"Reference product '{closest_name}' not found.")
            return None

        ref_price = ref_price.values[0]

        price_range = (0.8 * ref_price, 1.2 * ref_price)

        price_filtered_df = name_filtered_df[
            (name_filtered_df["price_per_serving"] >= price_range[0]) &
            (name_filtered_df["price_per_serving"] <= price_range[1])
        ]

        sorted_result = price_filtered_df.sort_values(by=column_name, ascending=True)

        #exclude the original product from the recommednations. if there are duplicates of the of product in the same shelf, it will dorp both
        sorted_result = sorted_result[sorted_result["product"].str.lower() != product_name.lower()]
        print({'ranking': sorted_result["product"].to_list()[:5]})

        return {'ranking': sorted_result["product"].to_list()[:5]}
