import pytest
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from service import chatService

client: TestClient = TestClient(app)


# mock response from chat service when searching 'orange juice'
mock_response = {
    "ranking": [
        "Tropicana Trop50 No Pulp Calcium + Vitamin D Orange Juice, 89 Oz Bottle",
        "Goodbelly Probiotics No Sugar Added Peach Mango Orange Juice Drink, 1 Quart"
    ]
}


# object which mocks the behavior of the chat service, assuming we are searching 'orange juice'
@pytest.fixture
def mock_chat_service():
    mock_service = MagicMock(spec=chatService)
    mock_service.getChatResponse.return_value = mock_response
    return mock_service


# mock chat service which throws an exception
@pytest.fixture
def mock_chat_service_exception():
    class MockChatService:
        def getChatResponse(self, query):
            raise ValueError("Simulated chat failure")
    return MockChatService()


def test_create_ranking_success(mock_chat_service):
    # override real dependencies with just the mock chat service for this test
    app.dependency_overrides[chatService] = lambda: mock_chat_service

    response = client.post("/grocery", json={"search_string": "orange juice"})

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) == 2

    returned_names = [item["product"] for item in data["products"]]
    assert returned_names == mock_response["ranking"]

    # validate structure of the first product
    first = data["products"][0]
    expected_keys = {
        "department", "aisle", "shelf", "product", "price", "servingspercontainer",
        "servingsize", "energykcal", "fat", "saturatedfat", "transfat", "carbohydrates",
        "sugar", "salt", "fibre", "protein", "ingredients", "redmeat", "shelfrank",
        "packsize", "packunit", "image", "energykcal per 100", "fat per 100",
        "saturatedfat per 100", "transfat per 100", "carbohydrates per 100",
        "sugar per 100", "salt per 100", "fibre per 100", "protein per 100",
        "ultra_processed_flag", "high_sugar_flag", "high_sodium_flag",
        "high_saturated_fat_flag", "high_calories_flag", "nns_flag"
    }

    # make sure the first product contains at least all of the expected keys
    assert expected_keys.issubset(set(first.keys()))

    # cleanup
    app.dependency_overrides = {}


def test_product_matching_order_preserved():
    # mock data frame
    data = [
        {"product": "Tropicana Trop50 No Pulp Calcium + Vitamin D Orange Juice, 89 Oz Bottle", "price": 5.18},
        {"product": "Goodbelly Probiotics No Sugar Added Peach Mango Orange Juice Drink, 1 Quart", "price": 2.98},
        {"product": "Minute Maid, Premium Strawberry Lemonade, 59 Fl. Oz.", "price": 1.50},
        {"product": "Simply Limeade, Non-Gmo, 52 Fl Oz", "price": 2.34}
    ]
    mock_df = pd.DataFrame(data)

    # mock ai ranking
    ranked_names = [
        "Goodbelly Probiotics No Sugar Added Peach Mango Orange Juice Drink, 1 Quart",
        "Tropicana Trop50 No Pulp Calcium + Vitamin D Orange Juice, 89 Oz Bottle"
    ]

    # matched products
    matched = mock_df[mock_df["product"].isin(ranked_names)]

    ranked_detailed = []
    for name in ranked_names:
        product_row = matched[matched["product"] == name]
        if not product_row.empty:
            ranked_detailed.append(product_row.iloc[0].to_dict())

    # assert that results are in the same order as ranked_names
    assert len(ranked_detailed) == 2
    assert ranked_detailed[0]["product"] == ranked_names[0]
    assert ranked_detailed[1]["product"] == ranked_names[1]


def test_create_ranking_exception():
    # send data with an empty search string to trigger an exception
    response = client.post("/grocery", json={"search string": ""})

    # make sure we get a status code 422 (Unprocessable Entity)
    assert response.status_code == 422


def test_create_ranking_chat_fail(mock_chat_service_exception):
    # override real dependencies with just the mock chat service for this test
    app.dependency_overrides[chatService] = lambda: mock_chat_service_exception

    response = client.post("/grocery", json={"search_string": "apple juice"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Simulated chat failure"

    # cleanup
    app.dependency_overrides = {}
