from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Ingredient:
  """Class representing an ingredient with name and amount (mL)"""
  name: str
  amount: int
  unit: str

@dataclass(frozen=True)
class CocktailRecipe:
  """Dataclass representing a cocktail recipe"""
  name: str
  base: str
  description: str
  summary: str
  ingredients: dict[str, str]
  tags: list[str]
  origin_country: str
  steps: list[str]
  external_link: str
  garnish: str
  glass_type: str