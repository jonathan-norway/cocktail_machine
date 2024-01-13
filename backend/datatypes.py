from dataclasses import dataclass, field
from typing import List, Dict, NamedTuple


@dataclass(frozen=True)
class CocktailRecipe:
    """Dataclass representing a cocktail recipe"""
    name: str
    base: str
    description: str
    summary: str
    origin_country: str
    external_link: str
    garnish: str
    glass_type: str
    tags: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    ingredients: dict[str, int] = field(default_factory=dict)


from datetime import datetime


from enum import Enum


class ValidIngredientUnits(Enum):
    MILLILITER = "mL"
    PIECES = "pcs"
    UNKNOWN = ""


@dataclass
class ExternalIngredient:
    name: str = field(default="")
    amount: int = field(default=0)
    date_added: str = field(default=datetime.now().date().strftime("%Y-%m-%d"))
    unit: ValidIngredientUnits = field(default=ValidIngredientUnits.UNKNOWN)


@dataclass
class DrinkStatistics:
    name: str
    times_made: int


CocktailStatisticsWithRecipe = NamedTuple(
    "CocktailStatisticsWithRecipe",
    statistics=DrinkStatistics,
    recipe=CocktailRecipe)
