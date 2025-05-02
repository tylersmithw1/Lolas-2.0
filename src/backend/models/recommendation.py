"""Model for a product name and column name; used in /recommendations."""

from pydantic import BaseModel


class Recommendation(BaseModel):
    product_name: str
    column_name: str
