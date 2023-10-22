from enum import Enum, auto
color_palette = {
    "black": "#231F20",
    "white": "#F2F1E6",
    "blue": "#05A3AD"
}

class GuiViews(Enum):
    MAIN_MENU = 0
    DRINK_MENU = auto()
    CUSTOM_DRINK = auto()
    SHOTS = auto()
    UTILS = auto()
