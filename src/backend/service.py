import dotenv
from langchain_community.chat_models import BedrockChat
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from tools import *


# llm = ChatBedrockConverse(
#     model="amazon.nova-pro-v1:0",
#     temperature=0,
#     max_tokens=None,
#     region_name = "us-east-1"
# )


# messages = [
#     ("system", "You are a helpful translator. Translate the user sentence to French."),
#     ("human", "I love programming."),
# ]


# response = llm.invoke(messages)
# print(response.content)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of tools.py (same as main.py)
# file_path = os.path.join(BASE_DIR, "sub-products.xlsx") # Full path to the Excel file

# df = pd.read_excel(file_path)


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
        "such as sugar, sodium, and saturated fat content. You will use the data you receive and provide a ranked"
        "recommendation of products based on some standards. Do your best to combine these standards to optimize the ranking"
        "from most healthful to least healthful. Priotize low sugar, low sodium, low saturated fat, low calorie products,"
        "and non-ultra processed. These are found in the 'ultra_processed_flag', 'high_sugar_flag', 'high_sodium_flag',"
        "'high_saturated_fat_flag', and 'high_calories_flag' columns'. A value of 1 indicates True and 0 indicated False."
        "(For example 1 in the 'high_sugar_flag' column means the product is high in sugar and 0 means the product is"
        "low in sugar). Your output should include 1) the FULL product name from the 'product' column. For example,"
        "'Lenders Bagel Shop Bagels Blueberry Bagels 17.1 Oz. 6 Count' Do not include any other additional columns."
        "Your output should be formated as follows: 'some text <json> {ranked_products} </json> some more text'."
        "For example: 'Here is the ranking: <json> {ranked_products} </json>. Do not give insight into your thinking process,"
        "just the ranking. DO NOT HALLUCINATE OR MAKE UP INFORMATION. ONLY GO OFF ON THE DATA YOU ARE GIVEN."
    )

    # PROMPT = SystemMessage(content="For each row, list the value in the 'product' column in the data you are given. Make sure to list ALL OF THEM.")

    TOOLS = [initial_data_search]

    # will prpbbaly need a function here to make sure we structure the ai output for frontend use

    def getChatResponse(self, user_input):
        chat = self.getBedrockChat()
        agent = create_react_agent(chat, self.TOOLS, state_modifier=self.PROMPT)
        config = {"recursion_limit": self.RECURSION_LIMIT}
        messages = agent.invoke({"messages": [("user", user_input)]}, config)
        output = messages["messages"]
        #output = messages["messages"][-1].content
        return output
