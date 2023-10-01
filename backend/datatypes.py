from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Ingredient:
  """Class representing an ingredient with name and amount (mL)"""
  name: str
  amount: int

@dataclass
class CocktailRecipe:
  """Class representing a cocktail recipe"""
  name: str
  description: str
  ingredients: dict
  