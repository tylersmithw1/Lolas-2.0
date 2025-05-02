"Test for api endpoints"
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from services.chat_service import chatService
from services.recommendation_service import RecommendationService


client: TestClient = TestClient(app)
#tests for the /grocery endpoint
# mock response from chat service when searching 'orange juice'
chat_mock_response = {
    "ranking": [
        "Tropicana Trop50 No Pulp Calcium + Vitamin D Orange Juice, 89 Oz Bottle",
        "Goodbelly Probiotics No Sugar Added Peach Mango Orange Juice Drink, 1 Quart"
    ]
}


# object which mocks the behavior of the chat service, assuming we are searching 'orange juice'
@pytest.fixture
def mock_chat_service():
    mock_service = MagicMock(spec=chatService)
    mock_service.getChatResponse.return_value = chat_mock_response
    return mock_service



def test_create_ranking_success(mock_chat_service):
    """testing the /grocery endpoint with a successful response from the chat service"""
    # override real dependencies with just the mock chat service for this test
    app.dependency_overrides[chatService] = lambda: mock_chat_service

    response = client.post("/grocery", json={"search_string": "orange juice"})

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) == 2

    returned_names = [item["product"] for item in data["products"]]
    assert returned_names == chat_mock_response["ranking"]

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
    """testing that the order of the products returned matches the order of the ranked names"""
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
    """testing the /grocery endpoint with an invalid request"""
    # send data with an empty search string to trigger an exception
    response = client.post("/grocery", json={"search string": ""})

    # make sure we get a status code 422 (Unprocessable Entity)
    assert response.status_code == 422


def test_create_ranking_chat_fail():
    class MockChatResponseFailingService:
        def getChatResponse(self, user_input):
            raise Exception("Simulated chat failure")
    
    app.dependency_overrides[chatService] = lambda: MockChatResponseFailingService()
    
    response = client.post("/grocery", json={"search_string": "apple juice"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Simulated chat failure"
    
    # Clean up the dependency override
    app.dependency_overrides = {}


#tests for the /recommendations endpoint
mock_recommendations = {
    "ranking": [
        "Kool-Aid Bursts Berry Blue Artificially Flavored Drink, 6 Ct. Package",
        "Capri Sun Flavored Juice Drink Blend With Other Natural Flavors Variety Pack, 30 Ct. Box",
        "Apple & Eve 100% Juice, Variety Pack, 6.75 Fl Oz, Pack Of 32"
    ]
}

## object which mocks the behavior of the recommendationservice (recommendations by column part)
@pytest.fixture
def mock_rec_service():
    mock_service = MagicMock(spec=RecommendationService)
    mock_service.recomendations_by_column.return_value = mock_recommendations
    return mock_service


def test_get_recommendations_success(mock_rec_service):
    """Test for successful recommendations"""
    app.dependency_overrides[RecommendationService] = lambda: mock_rec_service
    
    # Test the endpoint with valid input
    response = client.post("/recommendations", json={"product_name": "Some juice product", "column_name": "sugar"})
    
    
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 3  

    # Check if the product names match the expected result
    expected_products = mock_recommendations["ranking"]
    returned_products = [item["product"] for item in data["products"]]
    assert returned_products == expected_products
    
    # Clean up the dependency override
    app.dependency_overrides = {}


def test_get_recommendations_no_match(mock_rec_service):
    """Test for no close match found"""
    app.dependency_overrides[RecommendationService] = lambda: mock_rec_service
    
    # Mock the service to return no recommendations
    mock_rec_service.recomendations_by_column.return_value = {"ranking": []}
    
    response = client.post("/recommendations", json={"product_name": "Nonexistent Product", "column_name": "sugar"})
    
    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert len(data["products"]) == 0  # No products returned
    
    # Clean up the dependency override
    app.dependency_overrides = {}


def test_get_recommendations_invalid_column(mock_rec_service):
    """Test for invalid column name (unsupported column)"""
    app.dependency_overrides[RecommendationService] = lambda: mock_rec_service

    response = client.post("/recommendations", json={
        "product_name": "A - Pepperoni Pizza",
        "column_name": "invalid_column"
    })

    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Invalid column name: invalid_column" in data["detail"]


    app.dependency_overrides = {}

# mock chat service which throws an exception
def test_get_recommendations_service_fail():
    class MockReccomendationFailingService:
        def recomendations_by_column(self, product_name, column_name):
            raise Exception("Simulated rec failure")
    
    app.dependency_overrides[RecommendationService] = lambda: MockReccomendationFailingService()
    
    response = client.post("/recommendations", json={"product_name": "A - Pepperoni Pizza", "column_name": "sugar"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Simulated rec failure"
    
    # Clean up the dependency override
    app.dependency_overrides = {}


#tests for the /ai-recommendations endpoint
ai_rec_mock_response = {
    "ranking": [
        "Seapak Popcorn Shrimp, Frozen, 28 Oz",
        "John Soules Foods Chicken Fajitas, 16oz (Frozen)",
        "Totino's Pizza Rolls, Triple Meat, 50 Rolls, 24.8 Oz Bag"
    ]
}


# object which mocks the behavior of the recommendation service (specifically the ai response part)
@pytest.fixture
def mock_ai_rec_service():
    mock_service = MagicMock(spec=RecommendationService)
    mock_service.getRecommendationResponse.return_value = ai_rec_mock_response
    return mock_service

def test_get_ai_recommendations_ranking_success(mock_ai_rec_service):
    """testing the /grocery endpoint with a successful response from the chat service"""
    # override real dependencies with just the mock chat service for this test
    app.dependency_overrides[RecommendationService] = lambda: mock_ai_rec_service

    response = client.post("/ai-recommendations", json={"full_product_name": "Tai Pei Pork Egg Rolls, 8 Count, 24.5 Oz"})

    assert response.status_code == 200
    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) == 3

    returned_names = [item["product"] for item in data["products"]]
    assert returned_names == ai_rec_mock_response["ranking"]

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

def test_product_matching_order_preserved_ai_recommendations():
    """testing that the order of the products returned matches the order of the ranked names from the ai recommednations"""
    # mock data frame
    data = [
        {"product": "Lollipop", "price": 1.18},
        {"product": "Apple", "price": 6.90},
        {"product": "Coconut milk", "price": 8.90},
        {"product": "Shrimp", "price": 12.34},
        {"product": "Pineapple", "price": 2.34},
        {"product": "Chicken", "price": 5.00},
        {"product": "Beef", "price": 7.00},
        {"product": "Fish", "price": 4.50},
        {"product": "Pork", "price": 3.50}]
    mock_df = pd.DataFrame(data)

    # mock ai ranking of recommendations
    ranked_recommendation_names = [
        "Apple",
        "Shrimp",
        "Chicken",
        "Beef",
        "Fish",
    ]

    # matched products
    matched = mock_df[mock_df["product"].isin(ranked_recommendation_names)]

    ranked_detailed = []
    for name in ranked_recommendation_names:
        product_row = matched[matched["product"] == name]
        if not product_row.empty:
            ranked_detailed.append(product_row.iloc[0].to_dict())

    # assert that results are in the same order as ranked_names
    assert len(ranked_detailed) == 5
    assert ranked_detailed[0]["product"] == ranked_recommendation_names[0]
    assert ranked_detailed[1]["product"] == ranked_recommendation_names[1]
    assert ranked_detailed[2]["product"] == ranked_recommendation_names[2]
    assert ranked_detailed[3]["product"] == ranked_recommendation_names[3]
    assert ranked_detailed[4]["product"] == ranked_recommendation_names[4]


def test_ai_recommendation_exception():
    """testing the /ai-recommendation endpoint with an invalid request"""
    # send data with an empty search string to trigger an exception
    response = client.post("/ai-recommendations", json={"full product name": ""}) #doesnt match full_product_name

    # make sure we get a status code 422 (Unprocessable Entity)
    assert response.status_code == 422


def test_ai_recommendation_chat_fail():
    class MockAiRecResponseFailingService:
        def getRecommendationResponse(self, product_name):
            raise Exception("Simulated chat failure")
    
    app.dependency_overrides[RecommendationService] = lambda: MockAiRecResponseFailingService()
    
    response = client.post("/ai-recommendations", json={"full_product_name": "shrimp rolls"})
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Simulated chat failure"
    
    # Clean up the dependency override
    app.dependency_overrides = {}