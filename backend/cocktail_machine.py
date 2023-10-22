import json
import sys
import os
from pathlib import Path
from pump import Pump
import logging
from datatypes import CocktailRecipe
from typing import List
logger = logging.getLogger(__name__)
logging.basicConfig(filename="cocktail_machine.log", encoding="utf-8", level=logging.DEBUG)
os.chdir(Path(__file__).parent)

PUMPS_FILE = "data/pumps.json"
COCKTAIL_RECIPES_FILE =  "data/cocktails.json"
STATISTICS_FILE = "data/statistics.json"

class CocktailMachine():
  def __init__(self):  
    self.load_pumps_and_ingredients()
    self.load_cocktail_recipes()
    self.load_statistics()
    
  def load_pumps_and_ingredients(self):
    pumps_dict = {}
    with open(PUMPS_FILE, mode="rt", encoding="utf-8") as f:
      pumps_dict = json.load(f)
    for bottle_name, pump_data in pumps_dict.items():
      pump = Pump(pump_data["pump_code"], bottle_name, pump_data["amount"])
      pumps_dict[bottle_name] = pump
    self.pumps_dict = pumps_dict
    
  
  def pour_cocktail(self, cocktail_name: str):
    logger.info("Pouring cocktail '" + cocktail_name + "...")
    try:
      cocktail_recipe: CocktailRecipe = self.get_cocktail_recipe(cocktail_name)
      logger.debug("0")
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
      
    
    
  def get_cocktail_recipe(self, cocktail_name: str) -> dict:
    if not cocktail_name in self.cocktail_recipes.keys():
      logger.error(f"Cocktail_name '{cocktail_name}' does not exist.")
      raise ValueError("Cocktail does not exist")
    cocktail_recipe = self.cocktail_recipes[cocktail_name]
    logger.debug(cocktail_recipe)
    return cocktail_recipe
  
  def load_cocktail_recipes(self):
    cocktail_recipes = {}
    with open(COCKTAIL_RECIPES_FILE, mode="rt", encoding="utf-8") as f:
      temp_cocktail_recipes = json.load(f)
    for cocktail_name, cocktail_data in temp_cocktail_recipes.items():
      has_all_ingredients = True
      required_ingredients = cocktail_data["ingredients"].keys()
      for ingredient in required_ingredients:
        if not self.pumps_dict.get(ingredient):
          has_all_ingredients = False
          logger.warn(f"Does not have required ingredient '{ingredient}' for cocktail '{cocktail_name}'")
      if has_all_ingredients:
        cocktail_recipes[cocktail_name] = cocktail_data
    self.cocktail_recipes = cocktail_recipes
    
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
  