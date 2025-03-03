import { useState } from "react";

function App() {
  const [search, setSearch] = useState("");
  const [products, setProducts] = useState([]);

  // Function to fetch product data when Search button is clicked
  const fetchProducts = async () => {
    if (!search.trim()) {
      alert("Please enter a search term.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/product-info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ search_string: search }),
      });

      if (!response.ok) throw new Error("Failed to fetch");

      const data = await response.json();
      setProducts(data.products);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h1>Search for Product</h1>
      <input
        type="text"
        placeholder="Type to search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "80%",
          padding: "10px",
          fontSize: "16px",
          marginBottom: "10px",
        }}
      />
      <button
        onClick={fetchProducts}
        style={{
          marginLeft: "10px",
          padding: "10px 15px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        Search
      </button>

      {/* Display product results */}
      <div style={{ marginTop: "20px" }}>
        {products.length > 0 ? (
          products.map((product, index) => (
            <div key={index} style={{ padding: "10px", borderBottom: "1px solid #ddd" }}>
              {product.product}
            </div>
          ))
        ) : (
          <p>No results found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
