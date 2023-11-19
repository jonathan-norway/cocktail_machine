import os
from enum import Enum, auto

color_palette = {
    "black": "#231F20", "white": "#F2F1E6", "blue": "#05A3AD", "button-color": "#0095f"
}
MAX_WIDTH = 1024
MAX_HEIGHT = 550
current_directory = os.path.dirname(__file__)


class GuiViews(Enum):
    MAIN_MENU = 0
    DRINK_MENU = auto()
    CUSTOM_DRINK = auto()
    SHOTS = auto()
    UTILS = auto()


base_alcohols = [
    {
        "name": "vodka",
        "description": "Flavorless and distilled from potatoes.",
        "icon": current_directory + "/icons/vodka.png",
    },
    {
        "name": "gin",
        "description": "Dry and herby, and distilled from grain.",
        "icon": current_directory + "/icons/gin.png",
    },
    {
        "name": "rum",
        "description": "Sweet and distilled from sugar.",
        "icon": current_directory + "/icons/rum.png",
    },
    {
        "name": "tequila",
        "description": "Robust flavor and made from fermented agave",
        "icon": current_directory + "/icons/tequila.png",
    },
    {
        "name": "whiskey",
        "description": "Smooth and warm, and distilled from malted grains.",
        "icon": current_directory + "/icons/whiskey.png",
    },
]
