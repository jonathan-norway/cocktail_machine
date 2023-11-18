import json
import sys
import os
from pathlib import Path
from .pump import Pump
import logging
from .datatypes import CocktailRecipe, ExternalIngredient
from typing import List, Dict


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode="w",
    filename="cocktail_machine.log",
    encoding="utf-8",
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


current_directory = Path(__file__).parent

PUMPS_FILE = current_directory / "data/pumps.json"
COCKTAIL_RECIPES_FILE = current_directory / "data/cocktails.json"
STATISTICS_FILE = current_directory / "data/statistics.json"
BASE_ALCOHOLS_FILE = current_directory / "data/base_alcohols.json"
INGREDIENTS_FILE = current_directory / "data/ingredients.json"


class CocktailMachineSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if CocktailMachineSingleton.__instance is None:
            CocktailMachineSingleton.__instance = CocktailMachineClass()
            logger.warn("Created new instance of cocktail machine")
        else:
            logger.info("Reused cocktail machine instance")
        return CocktailMachineSingleton.__instance


class CocktailMachineClass():

    def __init__(self):
        self.load_ingredients()
        self.load_pumps()
        self.load_cocktail_recipes()
        self.load_statistics()

    def load_pumps(self):
        self.pumps_dict: Dict[str, Pump] = {}
        temp_pumps_dict = CocktailMachineClass.read_file(PUMPS_FILE)
        for _, pump_data in temp_pumps_dict.items():
            pump = Pump(**pump_data)
            self.pumps_dict[pump_data["contains"]] = pump

    @staticmethod
    def read_file(file_path: str):
        with open(file_path, mode="rt", encoding="utf-8") as f:
            temp_dictionary: dict = json.load(f)
        return temp_dictionary

    def load_ingredients(self):
        self.ingredients_dict: dict[str, ExternalIngredient] = {}
        temp_ingredients_dict = CocktailMachineClass.read_file(INGREDIENTS_FILE)
        for name, data in temp_ingredients_dict.items():
            ingredient = ExternalIngredient(name, **data)
            self.ingredients_dict[name] = ingredient

    def pour_cocktail(self, cocktail_name: str):
        logger.info("Pouring cocktail '" + cocktail_name + "...")
        try:
            cocktail_recipe: CocktailRecipe = self.get_cocktail_recipe(cocktail_name)
            # logger.debug("0")
            for ingredient, amount in cocktail_recipe.ingredients.items():
                pump: Pump = self.pumps_dict.get(ingredient)
                if pump is None:
                    self._check_enough_of_ingredient(ingredient, amount)
                else:
                    pump.assert_enough_amount(amount)
                logger.warn("yega")
            for ingredient, amount in cocktail_recipe.ingredients.items():
                pump = self.pumps_dict.get(ingredient)
                if pump is None:
                    logger.info(
                        f"There is no pump for {ingredient}. It has to be added manually after...")
                else:
                    pump.pour_amount(amount)
            self.update_statistics(cocktail_name)
            self.update_pumps()
            logger.info("Successfully poured cocktail " + cocktail_name)
        except Exception as e:
            logger.error(f"Could not pour cocktail {cocktail_name}: {str(e)}")
            raise e
        return "POURED"

    def _check_enough_of_ingredient(self, ingredient_name: str, amount_needed: int) -> None:
        assert ingredient_name in self.ingredients_dict.keys()
        assert int(amount_needed) <= int(self.ingredients_dict[ingredient_name])

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
        return
        statistics[drink_name] = statistics.get(drink_name, 0) + 1
        with open(STATISTICS_FILE, mode="wt", encoding="utf-8") as f:
            json.dump(statistics, f)
        self.statistics = statistics

    def update_pumps(self) -> None:
        pumps = self.pumps_dict
        return
        temp_dict = {}
        # for bottle, pump in pumps.items():
        #    temp_dict[bottle] = pump.as_dict()
        with open(PUMPS_FILE, mode="wt", encoding="utf-8") as f:
            json.dump(pumps, f)

    def load_statistics(self):
        with open(STATISTICS_FILE, mode="rt", encoding="utf-8") as f:
            statistics_from_file = json.load(f)
        self.statistics = statistics_from_file if statistics_from_file else {}

    def _test_i2c(self, alcohol_name: str, milliseconds: int) -> None:
        pump = self.pumps_dict[alcohol_name]
        pump._send_pump_event_with_milliseconds(milliseconds)

    def get_ingredients(self) -> List[ExternalIngredient]:
        return [ingredient for ingredient in self.ingredients_dict.values()
                ]

    def update_ingredient(self, ingredient: ExternalIngredient):
        logger.info(f"Updating ingredient '{ingredient}'")
        self.ingredients_dict[ingredient.name] = ingredient

    def remove_ingredient(self, ingredient_name: str):
        ingredient_to_remove = self.ingredients_dict.get(ingredient_name)
        logger.info(f"Removing ingredient '{ingredient_name} - {ingredient_to_remove}'")
        if ingredient_to_remove is None:
            logger.warning(f"Tried removing a non existing ingredient - {ingredient_name}")
            return
        del self.ingredients_dict[ingredient_name]


CocktailMachine = CocktailMachineSingleton.get_instance()
