"""Model for a grocery search term. Used in /grocery"""

from pydantic import BaseModel


class GrocerySearch(BaseModel):
    search_string: str
