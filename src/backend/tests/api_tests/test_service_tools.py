"Test for the service layer"
import pytest
from services.chat_service import chatService
from tools.tools import initial_data_search
from unittest.mock import patch, MagicMock
# from src.backend.service import chatService
# from src.backend.tools import initial_data_search

@pytest.fixture

def service():
    return chatService()


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


@patch("chatService.create_react_agent")
@patch.object(chatService, 'getBedrockChat')
def test_get_chat_response(mock_get_chat, mock_create_agent, service):
    """we need docstrings here"""
    mock_agent = MagicMock
    mock_agent.invoke.return_value = {
        "messages": [
            {"content": "Initial"},
            {"content": "Here is the ranking: <json> {'ranking': ['Product A', 'Product B']} </json>"}
        ]
    }
    mock_create_agent.return_value = mock_agent
    mock_get_chat.return_value = MagicMock()



@patch("service.ChatBedrockConverse")
def test_get_bedrock_chat(mock_chat, service):
    """we need docstrings here"""
    mock_llm = MagicMock()
    mock_chat.return_value = mock_llm
    result = service.getBedrockChat()

    # Confirm ChatBedrockConverse was called with expected parameters
    mock_chat.assert_called_once_with(
        model="amazon.nova-pro-v1:0",
        temperature=0,
        max_tokens=None,
        region_name="us-east-1",

    )
    # Confirm the returned object is what we mocked
    assert result == mock_llm