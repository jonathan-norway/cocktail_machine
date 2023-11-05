import json
import sys
import os
from pathlib import Path
from .pump import Pump
import logging
from .datatypes import CocktailRecipe
from typing import List
logger = logging.getLogger(__name__)
logging.basicConfig(filename="cocktail_machine.log", encoding="utf-8", level=logging.DEBUG)
os.chdir(Path(__file__).parent)

PUMPS_FILE = "data/pumps.json"
COCKTAIL_RECIPES_FILE = "data/cocktails.json"
STATISTICS_FILE = "data/statistics.json"
BASE_ALCOHOLS_FILE = "data/base_alcohols.json"
INGREDIENTS_FILE = "data/ingredients.json"


class CocktailMachineSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if CocktailMachineSingleton.__instance is None:
            __instance = CocktailMachineClass()
            logger.warn("Created new instance of cocktail machine")
        else:
            logger.info("Reused cocktail machine instance")
        return __instance


class CocktailMachineClass():

    def __init__(self):
        self.load_ingredients()
        self.load_pumps()
        self.load_cocktail_recipes()
        self.load_statistics()

    def load_pumps(self):
        self.pumps_dict = {}
        temp_pumps_dict = self.read_file(PUMPS_FILE)
        for bottle_name, pump_data in temp_pumps_dict.items():
            pump = Pump(pump_data["pump_code"], bottle_name, pump_data["amount"])
            self.pumps_dict[bottle_name] = pump

    def read_file(file_path: str):
        with open(file_path, mode="rt", encoding="utf-8") as f:
            temp_dictionary: dict = json.load(f)
        return temp_dictionary

    def load_ingredients(self):
        self.ingredients_dict = {}
        with open(INGREDIENTS_FILE, mode="rt", encoding="utf-8") as f:
            ingredients_dict: dict = json.load(f)
        for ingredient, amount in ingredients_dict.items():
            self.ingredients_dict[ingredient] = amount

    def pour_cocktail(self, cocktail_name: str):
        logger.info("Pouring cocktail '" + cocktail_name + "...")
        try:
            cocktail_recipe: CocktailRecipe = self.get_cocktail_recipe(cocktail_name)
            # logger.debug("0")
            for ingredient, amount in cocktail_recipe["ingredients"].items():
                pump: Pump = self.pumps_dict[ingredient]
                pump.assert_enough_amount(amount)
                logger.warn("yega")
            logger.debug("1")
            for ingredient, amount in cocktail_recipe["ingredients"].items():
                pump: Pump = self.pumps_dict[ingredient]
                pump.pour_amount(amount)
            logger.debug("2")
            self.update_statistics(cocktail_name)
            logger.debug("3")
            self.update_pumps()
            logger.info("Successfully poured cocktail " + cocktail_name)
        except Exception as e:
            logger.error(f"Could not pour cocktail {cocktail_name}: {str(e)}")

    def get_cocktail_recipe(self, cocktail_name: str) -> CocktailRecipe:
        try:
            cocktail_recipe = self.cocktail_recipes[cocktail_name]
        except Exception as e:
            logger.error(f"Cocktail_name '{cocktail_name}' does not exist.")
            logger.error(e)
            return None
        return cocktail_recipe

    def get_cocktail_recipes(self) -> dict[str, CocktailRecipe]:
        logger.debug("Got all cocktails")
        return self.cocktail_recipes

    def get_cocktail_recipes_by_base(self, base_alcohol: str) -> dict[str, CocktailRecipe]:
        logger.debug(f"Got cocktails by base ({base_alcohol})")
        cocktails = self.get_cocktail_recipes()
        filtered_cocktails = {cocktail_name: cocktail_data
                              for cocktail_name, cocktail_data in cocktails.items()
                              if cocktail_data.base.lower() == base_alcohol.lower()}
        return filtered_cocktails

    def get_cocktail_recipe_by_name(self, cocktail_name: str) -> CocktailRecipe:
        logger.debug(f"Got cocktail by name ({cocktail_name})")
        cocktails = self.get_cocktail_recipes()
        cocktail_recipe = cocktails.get(cocktail_name)
        assert cocktail_recipe is not None
        return cocktail_recipe

    def load_cocktail_recipes(self):
        cocktail_recipes: dict[str, CocktailRecipe] = {}
        with open(COCKTAIL_RECIPES_FILE, mode="rt", encoding="utf-8") as f:
            temp_cocktail_recipes: dict[str, dict] = json.load(f)

        for cocktail_name, cocktail_data in temp_cocktail_recipes.items():
            cocktail = CocktailRecipe(name=cocktail_name, **cocktail_data)

            has_all_ingredients = self.check_if_have_all_ingredients(cocktail.ingredients)
            if has_all_ingredients:
                cocktail_recipes[cocktail_name] = cocktail
            else:
                logger.warn(f"Missing ingredients for cocktail '{cocktail_name}'")
        self.cocktail_recipes = cocktail_recipes

    def check_if_have_all_ingredients(self, ingredients: dict[str, str]) -> bool:
        has_all_ingredients = True
        for ingredient, amount in ingredients.items():
            if not (self.pumps_dict.get(ingredient) or self.ingredients_dict.get(ingredient)):
                logger.warn(f"\tDoes not have required ingredient '{ingredient}'")
                has_all_ingredients = False

        return has_all_ingredients

    def update_statistics(self, drink_name: str) -> None:
        statistics = self.statistics
        statistics[drink_name] = statistics.get(drink_name, 0) + 1
        with open(STATISTICS_FILE, mode="wt", encoding="utf-8") as f:
            json.dump(statistics, f)
        self.statistics = statistics

    def update_pumps(self) -> None:
        pumps = self.pumps_dict
        temp_dict = {}
        for bottle, pump in pumps.items():
            temp_dict[bottle] = pump.as_dict()
        with open(PUMPS_FILE, mode="wt", encoding="utf-8") as f:
            json.dump(temp_dict, f)

    def load_statistics(self):
        with open(STATISTICS_FILE, mode="rt", encoding="utf-8") as f:
            statistics_from_file = json.load(f)
        self.statistics = statistics_from_file if statistics_from_file else {}


CocktailMachine = CocktailMachineSingleton.get_instance()
