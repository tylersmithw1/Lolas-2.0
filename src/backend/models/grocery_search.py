"""Model for a grocery search term."""
from pydantic import BaseModel


class GrocerySearch(BaseModel):
    search_string: str