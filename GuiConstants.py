from enum import Enum, auto

color_palette = {"black": "#231F20", "white": "#F2F1E6", "blue": "#05A3AD"}
MAX_WIDTH = 1024
MAX_HEIGHT = 600


class GuiViews(Enum):
    MAIN_MENU = 0
    DRINK_MENU = auto()
    CUSTOM_DRINK = auto()
    SHOTS = auto()
    UTILS = auto()


base_alcohols = [
    {
        "name": "vodka",
        "description": "Distilled primarily from high-starch plants, vodka typically isn't very flavorful. Potatoes are the most common base, though one can also use rye, corn, grains, or beets.",
        "icon": "icons/cocktail.png",
    },
    {
        "name": "gin",
        "description": "Gin is distilled from grain. Unflavored gin typically has a dry flavor with hints of juniper, citrus, or even malt wine, depending on how it was made. Many gins may also taste slightly sweet and can be flavored with a range of different spices or fruits.",
        "icon": "icons/cocktail.png",
    },
    {
        "name": "rum",
        "description": "Rum is typically distilled from some type of sugar, commonly either molasses or sugar cane. It tastes much sweeter than most other distilled spirits as a result.",
        "icon": "icons/cocktail.png",
    },
    {
        "name": "tequila",
        "description": "Made from fermented agave, tequila tastes somewhat sweet, earthy, and piquant, though this varies depending on where the agave was grown. Tequila has a reputation for being on the more robust end as spirits go.",
        "icon": "icons/cocktail.png",
    },
    {
        "name": "whiskey",
        "description": "Brewed by distilling malted grains such as rye, corn, wheat, or barley, whiskey is among the most diverse spirits on the list, with a distinctive flavor that depends mainly on where it's brewed",
        "icon": "icons/cocktail.png",
    },
]
