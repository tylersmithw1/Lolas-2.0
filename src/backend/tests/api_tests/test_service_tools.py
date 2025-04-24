"Test for the service layer"
import pytest
from services.chat_service import chatService
from services.recommendation_service import RecommendationService
from tools.tools import initial_data_search
from unittest.mock import patch, MagicMock
from langchain.schema import AIMessage, HumanMessage
import pandas as pd
import json
import numpy as np


#chatService tests
@pytest.fixture
def chat_service():
    return chatService()


@pytest.fixture
def search_mock_df():
    data = {
        "product": [
            "Ice Mountain Brand 100% Natural Spring Water, 16.9-Ounce Bottles (Pack Of 32)",
            "Coca Cola Classic 12oz Cans",
            "Organic Almond Milk Unsweetened",
            "Peanut Butter Crunchy Jar 16oz",
            "Propel Electrolyte Water, Kiwi Strawberry, 16.9 Oz Bottles, 12 Count",
            "Aquafina Purified Water, 16.9 Fl Oz Bottles, 32 Count"
        ]
    }
    return pd.DataFrame(data)


def test_extract_json_valid(chat_service):
    """test for valid JSON extraction"""
    response = "Here is the ranking: <json> {'ranking': ['Product A', 'Product B', 'Product C']} </json>"
    result = chat_service.extract_json(response)

    assert result == {'ranking': ['Product A', 'Product B', 'Product C']}


def test_extract_json_invalid(chat_service):
    """test for invalid JSON extraction"""
    response = "Sandy sells sea shells by the sea shore"
    result = chat_service.extract_json(response)
    assert result is None


def test_extract_json_bad_json(chat_service):
    """test for invalid JSON format"""
    response = "<json> {'ranking': ['Product A', Product B']} </json>"  # missing a quote around Product B
    result = chat_service.extract_json(response)
    assert result is None


@patch("services.chat_service.create_react_agent")
@patch.object(chatService, 'getBedrockChat')
def test_get_chat_response(mock_get_chat, mock_create_agent, chat_service):
    """tests for correctly calls agent and parses AI JSON from response."""
    
    # Mock LLM (this will be returned by `getBedrockChat()`)
    mock_llm = MagicMock()
    mock_get_chat.return_value = mock_llm
    
    # Mock agent and its invoke response
    mock_agent = MagicMock()
    # Simulating the response with different types of content (string and list)
    mock_agent.invoke.return_value = {
    "messages": [
        HumanMessage(content="pepperoni pizza"),
        AIMessage(content=[
            {"type": "text", "text": "<thinking> To rank the healthfulness of pepperoni pizza..."},
            {"type": "tool_use", "name": "initial_data_search", "input": {"query": "pepperoni pizza"}}
        ]),
        AIMessage(content="<thinking> Based on the retrieved data, I will rank the pepperoni pizza products...</thinking>\n\n<json> {'ranking': ['Real Good Pepperoni Pizza Snack Bites', 'Pepperoni Pizza Snack Rolls'] } </json>")
    ]
}
    mock_create_agent.return_value = mock_agent

    # Run the method with the mock data
    result = chat_service.getChatResponse("Rank the products")

    # Assert the correct JSON ranking is returned
    assert result == {'ranking': ['Real Good Pepperoni Pizza Snack Bites', 'Pepperoni Pizza Snack Rolls']}  


@patch("services.chat_service.ChatBedrockConverse")
def test_get_bedrock_chat(mock_chat, chat_service):
    """tests for returning a ChatBedrockConverse instance with correct params."""
    mock_llm = MagicMock()
    mock_chat.return_value = mock_llm
    result = chat_service.getBedrockChat()

    mock_chat.assert_called_once_with(
        model="amazon.nova-pro-v1:0",
        temperature=0,
        max_tokens=None,
        region_name="us-east-1",

    )
    # Confirm the returned object is what we mocked
    assert result == mock_llm

#tests for the 'tool' that chat service uses in the ai-agent
def test_initial_data_search_exact_match(search_mock_df):
    """test for exact match"""
    query = "Coca Cola Classic 12oz Cans"
    result = initial_data_search.invoke({"query": query, "df": search_mock_df, "threshold": 95})
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["product"] == "Coca Cola Classic 12oz Cans"


def test_initial_data_search_no_match(search_mock_df):
    """test for no match"""
    query = "Takis"
    result = initial_data_search.invoke({"query": query, "df": search_mock_df, "threshold": 90})
    assert result is None or json.loads(result) == []


def test_intiial_data_search_multiple_matches(search_mock_df):
    """test for multiple matches"""
    query = "Water"
    result = initial_data_search.invoke({"query": query, "df": search_mock_df, "threshold": 80})
    data = json.loads(result)
    assert all("water" in item["product"].lower() for item in data)


def test_initial_data_search_partial_match(search_mock_df):
    """test for partial match"""
    query = "kiwi strawberry"
    result = initial_data_search.invoke({"query": query, "df": search_mock_df, "threshold": 80})
    data = json.loads(result)
    assert any("Kiwi Strawberry" in item["product"] for item in data)
    assert "Kiwi Strawberry" in data[0]["product"]

#tests for the recommendation service
@pytest.fixture
def recommender_service():
    return RecommendationService()


@pytest.fixture
def recs_mock_df():
    data = {
        "product": [
            "A - Pepperoni Pizza", "B - Veggie Pizza", "C - Cheese Pizza",
            "D - Meat Lovers", "E - Supreme Pizza"
        ],
        "shelf": ["Frozen Pizza", "Frozen Pizza", "Frozen Pizza", "Frozen Pizza", "Frozen Pizza"],
        "price_per_serving": [3.0, 2.5, 3.2, 3.5, 3.1],
        "energykcal per 100": [250, 200, 230, 280, 240],
    }
    return pd.DataFrame(data)


def test_get_closest_product_match_found(recommender_service, recs_mock_df):
    """test for a close match found"""
    with patch("services.recommendation_service.process.extractOne") as mock_extract:
        mock_extract.return_value = ("A - Pepperoni Pizza", 90, 0)
        result = recommender_service.get_closest_product_name("pepperoni", recs_mock_df)
        assert result == "A - Pepperoni Pizza"

def test_get_closest_product_match_not_found(recommender_service, recs_mock_df):
    """test for no close match found"""
    with patch("services.recommendation_service.process.extractOne") as mock_extract:
        mock_extract.return_value = ("Simulated", 60, 0) #returns value below threshold, so should return None
        result = recommender_service.get_closest_product_name("xyz", recs_mock_df)
        assert result is None


@patch("services.recommendation_service.process.extractOne")
@patch("services.recommendation_service.TfidfVectorizer")
@patch("services.recommendation_service.cosine_similarity")
def test_recommendations_by_column_valid(mock_cosine, mock_vectorizer, mock_extract, recommender_service, recs_mock_df):
    """test for valid recommendations"""
    mock_extract.return_value = ("A - Pepperoni Pizza", 95, 0)

    mock_vec_instance = MagicMock()
    mock_vec_instance.transform.return_value = np.array([[1.0], [0.9], [0.8], [0.7], [0.6], [0.5]])
    mock_vectorizer.return_value = mock_vec_instance

    mock_cosine.return_value = np.array([[0.9, 0.85, 0.8, 0.03, 0.7]]) #assign similarity scores to the products. 'meat lovers' given a low similarity score here

    with patch("services.recommendation_service.DF", recs_mock_df):
        result = recommender_service.recomendations_by_column("A - Pepperoni Pizza", "energykcal per 100")

    assert isinstance(result, dict)  #make sure returns a dict
    assert "ranking" in result #make sure it has the ranking key
    #assert all("Pizza" in name for name in result["ranking"])  #assume recs will be pizza related
    assert "A - Pepperoni Pizza" not in result["ranking"]  # make sure the original product is excluded
    assert len(result["ranking"]) == 3  # 3 items are returned cause realistically all aside from 'meat lovers' should be similar (the word 'pizza' is in all of them)
    assert "D - Meat Lovers" not in result["ranking"]  # Ensure non-pizza products are excluded
    assert "B - Veggie Pizza" in result["ranking"]  # Ensure pizza-related products are included
    assert "C - Cheese Pizza" in result["ranking"]  # Ensure pizza-related products are included
    assert "E - Supreme Pizza" in result["ranking"]  # Ensure pizza-related products are included


@patch("services.recommendation_service.process.extractOne")
def test_recommendations_no_match(mock_extract, recommender_service):
    """test for no match found"""
    mock_extract.return_value = ("X", 40, 0)
    mock_df = pd.DataFrame({
        "product": [
            "A - Pepperoni Pizza", "B - Veggie Pizza", "C - Cheese Pizza",
            "D - Meat Lovers", "E - Supreme Pizza"
        ],
        "shelf": ["Frozen Pizza", "Frozen Pizza", "Frozen Pizza", "Frozen Pizza", "Frozen Pizza"],
        "price_per_serving": [3.0, 2.5, 3.2, 3.5, 3.1],
        "energykcal per 100": [250, 200, 230, 280, 240],
    })

    with patch("services.recommendation_service.DF", mock_df):
        result = recommender_service.recomendations_by_column("Unknown Product", "energykcal per 100")
        assert result is None

    

@patch("services.recommendation_service.create_react_agent")
@patch("services.recommendation_service.chatService.getBedrockChat")
@patch("services.recommendation_service.chatService.extract_json")
def test_get_recommendation_response(mock_extract_json, mock_get_chat, mock_create_agent, recommender_service):
    """Tests that RecommendationService correctly calls the agent and parses AI JSON from response."""

    # Mock LLM returned by getBedrockChat
    mock_llm = MagicMock()
    mock_get_chat.return_value = mock_llm

    # Mock agent and its invoke response
    mock_agent = MagicMock()
    mock_agent.invoke.return_value = {
        "messages": [
            HumanMessage(content="Real Good Pepperoni Pizza Snack Bites, 8.5 Oz Box, 8 Count"),
            AIMessage(content=[
                {"type": "text", "text": "<thinking> To recommend 5 healthier products..."},
                {"type": "tool_use", "name": "get_similar_shelf_products", "input": {"product_name": "Real Good Pepperoni Pizza Snack Bites, 8.5 Oz Box, 8 Count"}}
            ]),
            AIMessage(content="<thinking> Based on the retrieved data...</thinking>\n\n<json> {'ranking': ['Lean Cuisine Features Supreme Frozen Pizza 6 Oz.', 'Caulipower Cauliflower Pizza Crusts, 2 Pack, 11 Oz (Frozen)', 'Califlour Foods 2 Cauliflower Pizza Crusts, Plain Crust', 'Green Giantâ¢ Cauliflower Pizza Crust Tuscan 7.5 Box', 'Digiorno Pizzeria! Thin Hand-Tossed Crust Margherita Frozen Pizza 18 Oz. Box 18 Oz.']} </json>")
        ]
    }
    mock_create_agent.return_value = mock_agent

    # Patch extract_json to return expected parsed dict
    expected_result = {
        'ranking': [
            'Lean Cuisine Features Supreme Frozen Pizza 6 Oz.',
            'Caulipower Cauliflower Pizza Crusts, 2 Pack, 11 Oz (Frozen)',
            'Califlour Foods 2 Cauliflower Pizza Crusts, Plain Crust',
            'Green Giantâ¢ Cauliflower Pizza Crust Tuscan 7.5 Box',
            'Digiorno Pizzeria! Thin Hand-Tossed Crust Margherita Frozen Pizza 18 Oz. Box 18 Oz.'
        ]
    }
    mock_extract_json.return_value = expected_result

    # Call the method and assert
    result = recommender_service.getRecommendationResponse("Real Good Pepperoni Pizza Snack Bites, 8.5 Oz Box, 8 Count")
    assert result == expected_result
