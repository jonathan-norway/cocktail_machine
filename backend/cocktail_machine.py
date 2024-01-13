import json
import sys
import os
from pathlib import Path
from .pump import Pump
import logging
from .datatypes import CocktailRecipe, ExternalIngredient, DrinkStatistics, CocktailStatisticsWithRecipe
from typing import List, Dict, NamedTuple
from dataclasses import asdict
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/backend.log', mode='w', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

current_directory = Path(__file__).parent

PUMPS_FILE = current_directory / "data/pumps.json"
PUMPS_FILE2 = current_directory / "data/pumps2.json"
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
        self._pumps_dict: Dict[str, Pump] = {}
        temp_pumps_dict = CocktailMachineClass.read_file(PUMPS_FILE)
        for _, pump_data in temp_pumps_dict.items():
            pump = Pump(**pump_data)
            contains = pump_data["contains"] if pump_data[
                "contains"] != "" else f"EMPTY_{uuid.uuid4()}"
            self._pumps_dict[contains] = pump

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
                pump: Pump = self._pumps_dict.get(ingredient)
                if pump is None:
                    self._check_enough_of_ingredient(ingredient, amount)
                else:
                    pump.assert_enough_amount(amount)
                logger.warn("yega")
            for ingredient, amount in cocktail_recipe.ingredients.items():
                pump = self._pumps_dict.get(ingredient)
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
            if not (self._pumps_dict.get(ingredient) or self.ingredients_dict.get(ingredient)):
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

    def _save_pumps(self) -> None:
        temp_dict = {}
        for i, pump in enumerate(self._pumps_dict.values()):
            temp_dict[f"pump{i}"] = asdict(pump)
        with open(PUMPS_FILE2, mode="wt", encoding="utf-8") as f:
            json.dump(temp_dict, f)

    def load_statistics(self):
        self.statistics: Dict[str, DrinkStatistics] = dict()
        with open(STATISTICS_FILE, mode="rt", encoding="utf-8") as f:
            statistics_from_file: dict = json.load(f)
        for cocktail_name, times_made in statistics_from_file.items():
            self.statistics[cocktail_name] = DrinkStatistics(cocktail_name, times_made)
        # self.statistics = statistics_from_file if statistics_from_file else {}

    def _test_i2c(self, alcohol_name: str, milliseconds: int) -> None:
        pump = self._pumps_dict[alcohol_name]
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

    def get_pumps(self):
        return [pump for pump in self._pumps_dict.values()]

    def update_pump(self, updated_pump: Pump):
        logger.info(f"Updating pump '{updated_pump}'")
        old_pump_key = [key for key, pump in self._pumps_dict.items() if pump.pump_code ==
                        updated_pump.pump_code][0]
        self._pumps_dict[old_pump_key] = updated_pump
        self._save_pumps()

    def get_most_popular_cocktails(self) -> List[DrinkStatistics]:
        return list(self.get_statistics().values()).sort(
            key=lambda drink_statistic: drink_statistic.times_made, reverse=True)

    def get_most_popular_available_cocktails(self) -> List[CocktailStatisticsWithRecipe]:
        cocktail_statistics = self.get_most_popular_cocktails()

        available_cocktails_by_popularity: List[CocktailStatisticsWithRecipe] = []
        for cocktail_statistic in cocktail_statistics:
            try:
                cocktail_recipe = self.get_cocktail_recipe(cocktail_statistic.name)
            except ValueError:
                logger.warning(
                    f"Cocktail recipe for cocktail statistics {cocktail_statistic!r} for available")
                continue
            available_cocktails_by_popularity.append(
                CocktailStatisticsWithRecipe(
                    statistics=cocktail_statistic,
                    recipe=cocktail_recipe))

        return available_cocktails_by_popularity

    def get_statistics(self):
        return self.statistics


CocktailMachine = CocktailMachineSingleton.get_instance()
