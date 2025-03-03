import "./ProductCard.css"; // Style your product cards

function ProductCard({ name }) {
  return (
    <div className="product-card">
      <h3>{name}</h3>
      {/* More details (price, ingredients) will go here later */}
    </div>
  );
}

export default ProductCard;
