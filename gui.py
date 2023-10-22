from guizero import App, ListBox, PushButton, Text, TextBox, Box
import sys
import os
sys.path.append(os.getcwd() + "/backend/")

from backend.cocktail_machine import CocktailMachine
cocktail_machine = CocktailMachine()


def display_drink_details(selected_drink_name):
    ingredients_textbox.clear()
    drink_description_textbox.clear()
    
    cocktail_recipe = cocktail_machine.get_cocktail_recipe(selected_drink_name)
    
    drink_description_textbox.value = cocktail_recipe.get("description", "No description available")
    for ingredient, amount in cocktail_recipe["ingredients"].items():
      ingredients_textbox.append(f"{ingredient}: {amount}mL\n")

def make_drink():
  cocktail_machine.pour_cocktail(listbox.value)

app = App(title="Hello World", width=1024, height=600, layout="grid")
left_box = Box(app, width=400, height=500, layout="grid", grid=[0,0], align="left")
right_box = Box(app, width=400, height=500, layout="grid", grid=[1,0], align="right")
listbox = ListBox(left_box,items=[drink_name for drink_name in cocktail_machine.cocktail_recipes.keys()], 
                command=display_drink_details, width=400, height=400, grid=[0,1])
drink_description_textbox = TextBox(right_box, width=400, height=200, multiline=True, scrollbar=True, grid=[1,1])
ingredients_textbox = TextBox(listbox, width=400, height=300, multiline=True, scrollbar=True)
make_button = PushButton(right_box, text="Make drink",grid=[0,0], command=make_drink)
app.display()

