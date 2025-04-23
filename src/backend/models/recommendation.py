"""Model for a grocery search term."""
from pydantic import BaseModel


class Recommendation(BaseModel):
    product_name: str
    column_name: str
