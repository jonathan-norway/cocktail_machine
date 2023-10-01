#!/usr/bin/python3
from guizero import App, Box, Text, PushButton
from ruamel.yaml import YAML

INGREDIENTS_FILE = "ingredients.yaml"
COCKTAILS_FILE = "cocktails.yaml"
SHOTS_FILE = "shots.yaml"
PUMP_CODES_FILE = "pump_codes.yaml"
  

class Pump():
  def __init__(self, pump_code: str, ingredient_name: str, amount: int):
    self.pump_code = pump_code
    self.ingredient_name = ingredient_name
    self.amount = amount
  
  def run_pump(self, amount_to_pour: int) -> None:
    self.amount -= amount_to_pour
    print(f"Ran pump #{self.pump_code} for {amount_to_pour}mL of {self.ingredient_name}")

class CocktailMachine():

  def __init__(self):
    load_files()
    
  def pour_ingredient(self, ingredient_name: str, amount: int) -> None:
    pump_code = self.get_pump_code(ingredient_name)
    self.send_pump_event(pump_code, amount)
    print(f"POURING {amount} of {ingredient_name}")
    
  def make_cocktail(self, cocktail_name: dict) -> None:
    cocktail_ingredients = self.cocktails.get(cocktail_name)
    for ingredient, amount in cocktail_ingredients.items():
      self.pour_ingredient(ingredient, amount)
  
  def get_pump_code(self, ingredient_name: str) -> str:
    return self.pump_codes.get(ingredient_name)
  
  def send_pump_event(self, pump_code: str, amount: int) -> None:
    print(f"SENT PUMP EVENT #{pump_code} {amount}mL")
  
  def load_files(self):
    self.load_ingredients()
    self.load_cocktails()
    self.load_shots()
    self.load_pump_codes()

  def load_ingredients(self) -> dict:
    self.ingredients = read_yaml_file(INGREDIENTS_FILE)

  def update_ingredients(self, updated_ingredients: dict) -> dict:
    self.ingredients = write_yaml_file(INGREDIENTS_FILE, updated_ingredients)
  

  def load_cocktails(self) -> dict:
    self.cocktails = read_yaml_file(COCKTAILS_FILE)

  def load_shots(self) -> dict:
    self.shots = read_yaml_file(SHOTS_FILE)  
    
  def load_pump_codes(self) -> dict:
    self.pump_codes = read_yaml_file(PUMP_CODES_FILE)  
  

def setup_yaml_reader() -> YAML:
  yaml_reader = YAML()
  yaml_reader.indent = 2
  return yaml_reader

def read_yaml_file(file_name: str) -> dict:
  yaml_reader = setup_yaml_reader()
  with open(file_name, "r") as f:
    return yaml_reader.load(f)

def write_yaml_file(file_name: str, content: dict) -> None:
  yaml_writer = setup_yaml_reader()
  with open(file_name, "w") as f:
    yaml_writer.dump(content, f)
  return content



def printer():
  print("print")

def initiate_gui():
  app = App(title="Hello World", width=1024, height=600)
  message = Text(app, text="Hello to the cocktail machine")
  button = PushButton(app, text="Press to print", command=printer)
  app.display()

def create_cocktail(cocktail_name: str) -> None:
  pass

def main():
  initiate_gui()

if __name__ == "__main__":
  main()
