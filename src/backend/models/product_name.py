"""Model for a product name; used for ai recs."""
from pydantic import BaseModel


class ProductName(BaseModel):
    full_product_name: str