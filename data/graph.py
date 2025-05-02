import pandas as pd
import networkx as nx

def build_food_graph(file_path):
    """
    Builds a knowledge graph from food product data.
    """
    # Load data
    df = pd.read_excel(file_path)
    G = nx.Graph()
    # Add nodes (products)
    for _, row in df.iterrows():
        G.add_node(
        row['product'],
        location=row['aisle'],
        price=row['price'],
        serving_info=row['Serving Size'],
        energy=row['energykcal'],
        fat=row['fat'],
        sat_fat=row['saturatedfat'],
        trans_fat=row['transfat'],
        carbs=row['carbohydrates'],
        salt=row['salt'],
        fibre=row['fibre'],
        protein=row['protein'],
        ingredients=row['ingredients'],
        red_meat=row['redmeat'],
        high_sugar=row['high_sugar_flag'],
        high_sodium=row['high_sodium_flag'],
        high_sat_fat=row['high_saturated_fat_flag'],
        high_calories=row['high_calories_flag'],
        ultra_processed=row['ultra_processed_flag']
        )
    # Add edges (relationships)
    for node1, node2 in nx.combinations(G.nodes, 2):
        data1, data2 = G.nodes[node1], G.nodes[node2]
        # Nutritional similarity (binary flags match)
        if any(data1[attr] == 1 and data2[attr] == 1 for attr in ['high_sugar', 'high_sodium', 'high_sat_fat', 'ultra_processed', 'high_calories']):
            G.add_edge(node1, node2, relationship='nutritional_similarity')
        # Price similarity (within 25%)
        if abs(data1['price'] - data2['price']) / max(data1['price'], data2['price']) <= 0.25:
            G.add_edge(node1, node2, relationship='price_similarity')
        # Packaging similarity
        if data1['serving_info'] == data2['serving_info']:
            G.add_edge(node1, node2, relationship='packaging_similarity')
        # Category similarity
        if data1['location'] == data2['location']:
            G.add_edge(node1, node2, relationship='category_similarity')
        return G

def query_graph(G, node_name, relationship_type):
    """
    Queries the graph for similar products based on a given relationship type.
    """
    return list(nx.neighbors(G, node_name)) if node_name in G else []

    # Example Usage
    # file_path = "your_excel_file.xlsx"
    # G = build_food_graph(file_path)
    # print(query_graph(G, 'Coca-Cola', 'nutritional_similarity'))