"Service methods to support api for lola's 2.0. This handles the chatbot ranking response."
import dotenv
from langchain_community.chat_models import BedrockChat
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
#from src.backend.tools.tools import *
from tools.tools import initial_data_search
import ast
import re


dotenv.load_dotenv()


class chatService:
    
    RECURSION_LIMIT = 2 * 100 + 1

    def getBedrockChat(self):
        llm = ChatBedrockConverse(
            model="amazon.nova-pro-v1:0",
            temperature=0,
            max_tokens=None,
            region_name="us-east-1",
        )
        return llm


    PROMPT = SystemMessage(
        content="You are an intelligent and detail-oriented grocery store assistant with a strong focus on nutrition and"
        "healthfulness. Your goal is to help users make informed, health-conscious choices by analyzing product attributes"
        "such as sugar, sodium, calorie content, saturated fat, and degree of processing. You will receive a product name. Use the 'inital_data_search' tool to receive the data of the products you will be ranking." 
        "The data you are given includes both binary flags (indicating whether a product is high in certain nutrients) and numeric values per 100g (e.g., fat per 100g, sugar per 100g)." 
        "You will use this to generate a ranked list of products from most healthful to least healthful. Do your best to combine these standards to optimize the ranking"
        "from most healthful to least healthful." 

        "Prioritize:" 
        "- low sugar (based on sugar per 100 and high_sugar_flag)" 
        "- low sodium (based on salt per 100 and high_sugar_flag)" 
        "- low saturated fat (based on saturatedfat per 100 and high_saturated_fat_flag)" 
        "- non-ultra processed (based on ultra_processed_flag = 0)" 
        "- low calories ONLY when combined with the other flags"

        "Use this as a guide to rank the products:" 
        "1) Use the actual numeric values per 100g of calories, per 100g of saturated fat, 100g of sugar, and 100g of saturated fat, and alongside their binary flags."
        "The per 100g calculations are found in the 'energykcal per 100', 'saturatedfat per 100',  'sugar per 100', and 'salt per 100' columns respectively."
        "The binary flags are found in the 'high_calories_flag', 'high_saturated_fat_flag', 'high_sugar_flag', and 'high_sodium_flag' columns respectively. Additionally, consider the 'ultra_processed_flag' column."
        "Remember that a value of 1 indicates True (high) and 0 indicates False (low)."

        "2) Products with higher numeric values of calories, sugar, sodium, and saturated fat should be ranked lower." 

        "3) Use the binary flags for calories, sugar, sodium, and saturated fat as additional cues, but do not rely on them alone. For ultraprocessed, only the binary flag is used"
        "For example, product A with with 450mg of sodium/100g is much 'better than product B with 950mg of sodium/100g, but they would both be flagged as high sodium. So it is important to consider the actual numeric values, while also using the binary flags as a guide."

        "4) A product with multiple concerning flags and high numeric values (e.g., high sugar and sodium) should rank lower than a product with only one issue."
        
        "5) High-calorie flag is ONLY a priority when present for a product with any of the other flags. A product with only the high_calories_flag set to 1 and no other flags should not be ranked poorly — this flag should only affect ranking when combined with another flag."
        "For example, product A flagged as high calorie and no other flags would be ranked higher than product B flagged as high calorie and flagged as high sugar, and high sodium."

        "6) Return the result of your ranking in a JSON format with the following exact structure: Make sure to include the <json> tags in your output. "
        "For example: 'Here is the ranking: <json> {'ranking': ['Product Name 1', 'Product Name 2', 'Product Name 3']} </json>. Do not give insight into your thinking process," 
    )
        
    




    TOOLS = [initial_data_search]

    def extract_json(self, response_text):
    # Step 1: Extract string between <json> and </json>
        match = re.search(r"<json>\s*(.*?)\s*</json>", response_text, re.DOTALL)

        if match:
            json_like_string = match.group(1)

            # Step 2: Convert string to dictionary safely
            try:
                data = ast.literal_eval(json_like_string)
                return data  # Return the parsed dictionary
            except Exception as e:
                print("Error parsing JSON:", e)
                return None
        else:
            print("No JSON block found.")
            return None
        


    def getChatResponse(self, user_input):
        chat = self.getBedrockChat()
        agent = create_react_agent(chat, self.TOOLS, state_modifier=self.PROMPT)
        config = {"recursion_limit": self.RECURSION_LIMIT, "timeout": 20*60}
        messages = agent.invoke({"messages": [("user", user_input)]}, config)
        output = messages["messages"]
        ai_output = messages["messages"][-1].content
        print(f"AI Output: {ai_output}")
        json_output = self.extract_json(ai_output)
        #return ai_output
        #return output
        return json_output


        
