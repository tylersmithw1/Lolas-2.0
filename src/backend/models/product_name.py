"""Model for a product name; used in /ai-recommendations"""

from pydantic import BaseModel


class ProductName(BaseModel):
    full_product_name: str
