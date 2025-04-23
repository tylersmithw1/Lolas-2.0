"Test for the service layer"
import pytest
from services.chat_service import chatService
from tools.tools import initial_data_search
from unittest.mock import patch, MagicMock
from langchain.schema import AIMessage, HumanMessage
import pandas as pd
import json


@pytest.fixture
def service():
    return chatService()


@pytest.fixture
def mock_df():
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


def test_extract_json_valid(service):
    """we need docstrings here"""
    response = "Here is the ranking: <json> {'ranking': ['Product A', 'Product B', 'Product C']} </json>"
    result = service.extract_json(response)

    assert result == {'ranking': ['Product A', 'Product B', 'Product C']}


def test_extract_json_invalid(service):
    """"we need docstrings here"""
    response = "Sandy sells sea shells by the sea shore"
    result = service.extract_json(response)
    assert result is None


def test_extract_json_bad_json(service):
    """we need docstrings here"""
    response = "<json> {'ranking': ['Product A', Product B']} </json>"  # missing a quote around Product B
    result = service.extract_json(response)
    assert result is None


@patch("services.chat_service.create_react_agent")
@patch.object(chatService, 'getBedrockChat')
def test_get_chat_response(mock_get_chat, mock_create_agent, service):
    """Correctly calls agent and parses AI JSON from response."""
    
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
    result = service.getChatResponse("Rank the products")

    # Assert the correct JSON ranking is returned
    assert result == {'ranking': ['Real Good Pepperoni Pizza Snack Bites', 'Pepperoni Pizza Snack Rolls']}  


@patch("services.chat_service.ChatBedrockConverse")
def test_get_bedrock_chat(mock_chat, service):
    """Returns a ChatBedrockConverse instance with correct params."""
    mock_llm = MagicMock()
    mock_chat.return_value = mock_llm
    result = service.getBedrockChat()

    mock_chat.assert_called_once_with(
        model="amazon.nova-pro-v1:0",
        temperature=0,
        max_tokens=None,
        region_name="us-east-1",

    )
    # Confirm the returned object is what we mocked
    assert result == mock_llm


def test_initial_data_search_exact_match(mock_df):
    query = "Coca Cola Classic 12oz Cans"
    result = initial_data_search.invoke({"query": query, "df": mock_df, "threshold": 95})
    data = json.loads(result)
    assert len(data) == 1
    assert "Coca Cola" in data[0]["product"]


def test_initial_data_search_no_match(mock_df):
    query = "Takis"
    result = initial_data_search.invoke({"query": query, "df": mock_df, "threshold": 90})
    assert result is None or json.loads(result) == []


def test_intiial_data_search_multiple_matches(mock_df):
    query = "Water"
    result = initial_data_search.invoke({"query": query, "df": mock_df, "threshold": 80})
    data = json.loads(result)
    assert all("water" in item["product"].lower() for item in data)


def test_initial_data_search_partial_match(mock_df):
    query = "kiwi strawberry"
    result = initial_data_search.invoke({"query": query, "df": mock_df, "threshold": 80})
    data = json.loads(result)
    assert any("Kiwi Strawberry" in item["product"] for item in data)
    assert "Kiwi Strawberry" in data[0]["product"]
