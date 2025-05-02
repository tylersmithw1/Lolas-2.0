"""Service methods to support api for lola's 2.0. This handles both the manual recommendations (by health attribute column) and the AI recommendations (which combines all the different health attribute columns) """


import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz, process
from tools.tools import get_similar_shelf_products
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from services.chat_service import chatService



BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
file_path = os.path.join(BASE_DIR, "recommendation_products.xlsx")  # Full path to the Excel file

REC_DF = pd.read_excel(file_path)

#products repeat in the dataset, sometimes appearing in different shelves. Here we use the first instance of the product's shelf name. so ultimately, need to find and drop duplicates
class RecommendationService:
    """Recommendation class."""
    def __init__(self):
        pass

    def get_closest_product_name(self, product_name, df, threshold=50):
        """Get the closest product name from the DataFrame using fuzzy matching."""
        product_list = df["product"].tolist()
        match, score, idx = process.extractOne(
            product_name, product_list, scorer=fuzz.token_sort_ratio
        )
        if score >= threshold:
            return match
        return None

    def recomendations_by_column(self, product_name, column_name):
        """Get recommendations based on a specific column. This is the method that will be called by the /recommendations API."""
        closest_name = self.get_closest_product_name(product_name, REC_DF)
        if not closest_name:
            print(f"No close match found for product '{product_name}'.")
            return None

        shelf_value = REC_DF.loc[REC_DF["product"] == closest_name, "shelf"].values[0]
        print(f"Closest product name: {closest_name}, Shelf: {shelf_value}")

        filtered_df = REC_DF[REC_DF["shelf"] == shelf_value].copy()

        names = filtered_df["product"].tolist()
        vectorizer = TfidfVectorizer().fit([closest_name] + names)
        vectors = vectorizer.transform([closest_name] + names)

        ref_vector = vectors[0]
        other_vectors = vectors[1:]

        similarities = cosine_similarity(ref_vector, other_vectors).flatten()
        filtered_df["name_similarity"] = similarities

        # Keep only those with sufficient similarity
        name_filtered_df = filtered_df[filtered_df["name_similarity"] >= 0.025]  #decrease number to increase # of recommendations

        ref_price = REC_DF[
            (REC_DF["product"].str.lower() == closest_name.lower()) &
            (REC_DF["shelf"].str.lower() == shelf_value.lower())
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

        #exclude the original product from the recommendations. if there are duplicates of the of product in the same shelf, it will dorp both
        sorted_result = sorted_result[sorted_result["product"].str.lower() != product_name.lower()]
        # ex = {'ranking': sorted_result[["product", "shelf"]].to_dict(orient='records')[:5]}
        # print(ex)

        return {'ranking': sorted_result["product"].to_list()[:4]}

    
    #use an instance of chatService here because the AI response uses the same algorithms as chatService. So there's no need to repeat the code
    CHAT_SERVICE = chatService()

    PROMPT = SystemMessage(
        content="You are an intelligent and detail-oriented food recommender with a strong focus on nutrition and"
        "healthfulness. Your goal is to rank and recommend users health-conscious food products by analyzing product attributes"
        "such as sugar, sodium, calorie content, saturated fat, degree of processing, and nns. You will receive a product name. Use the 'get_similar_shelf_products' tool to receive the data of the products" 
        "you will be ranking and recommending." 

        "Use this as a guide to rank the products and make recommendations:"
        "1) Extract the price_per_serving of the original product using the 'product' column to match the product name and the 'price_per_serving' column to find the corresponding price per serving" 
        "Use this as a reference point as ultimately, your recommendations should recommend products within 20 percent of the original product's price."

        "2) Take semantics into consideration. For example, if the product is 'pepperoni pizza', it is likely that the products retrieved from the get_similar_shelf_products tool will include non-pepperoni pizza products."
        "As such, it wouldn't make sense to recommend a lasagne product to a user looking for a pepperoni pizza recommendations. So it is important to consider the product name and its semantics when making recommendations."

        "3) Use the numeric values contained in the 'energykcal per 100', 'saturatedfat per 100',  'sugar per 100', and 'salt per 100' columns respectively."

        "4) Use the binary flags contained in the 'ultra_processed_flag' and 'nns_flag' columns respectively."

        "5) Combine both the numeric values and binary flags to generate a ranked list of products from most healthful to least healthful. Do your best to combine these standards to optimize the ranking and thus your recommendations."

        "6) Always return only 4 recommendations, essentially; the top 4 from your ranking."

        "7) Ultimately, you are making and returning a healthful ranking of 4 recommendations using the semantics of the product name, within 20 percent of the product price, and using the numeric values and binary flags of nutrition attriutes to rank the products from most healthful to least healthful."
        
        "8) Return the result of your ranking in a JSON format with the following exact structure: Make sure to include the <json> tags in your output. "
        "For example: 'Here is the recommendation: <json> {'ranking': ['Product Name 1', 'Product Name 2', 'Product Name 3']} </json>. Do not give insight into your thinking process," 

        
        )


    TOOLS = [get_similar_shelf_products] #This is how we give the AI agent 'tools' to use


    def getRecommendationResponse(self, product_name):
        """Get AI recommendations based on the product name. This is the method that will be called by the /ai-recommendations API."""
        chat = self.CHAT_SERVICE.getBedrockChat()
        agent = create_react_agent(chat, self.TOOLS, state_modifier=self.PROMPT)
        config = {"recursion_limit": self.CHAT_SERVICE.RECURSION_LIMIT, "timeout": 20*60}
        messages = agent.invoke({"messages": [("user", product_name)]}, config)
        output = messages["messages"]
        ai_output = messages["messages"][-1].content
        print(f"AI Output: {ai_output}")
        json_output = self.CHAT_SERVICE.extract_json(ai_output)
        return json_output


