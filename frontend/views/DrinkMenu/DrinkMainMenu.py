from enum import Enum, auto
from typing import Callable, List

from frontend.GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from backend import CocktailMachine

from frontend.components import (DrinkCard, MainMenu,
                                 MenuModeCard, ModeMenuLayout, SecondHeader, Card, CardList)
from .Modes import ModesMenu, BaseAlcoholMode, BaseAlcoholDrinkCard, ListDrinkDisplayMode, DetailedDrinkDisplayMode


class DrinkMenuModes(Enum):
    MAIN = 0
    BASE_ALCOHOL = auto()
    POPULARITY = auto()
    MOOD = auto()
    DISPLAY_LIST = auto()
    DISPLAY_DETAILED = auto()


from frontend.icons import icon_dict

import logging
logger = logging.getLogger(__name__)


class DrinkMenuView(MainMenu):
    def __init__(self):
        super(DrinkMenuView, self).__init__(title="Drinks")
        logger.info("Initializing DrinkMenuView")
        self._add_all_modes()
        logger.info("Finished initializing DrinkMenuView")

    def _add_all_modes(self):
        logger.info("Adding DrinkMenuView modes")
        self.add_mode(ModesMenu(self.inner_navigate))
        self.add_mode(BaseAlcoholMode(select_base_alcohol=self.get_and_display_drinks_by_base))
        self.add_mode(BaseAlcoholMode(select_base_alcohol=self.get_and_display_drinks_by_base))
        self.add_mode(BaseAlcoholMode(select_base_alcohol=self.get_and_display_drinks_by_base))
        self.add_mode(self.list_display_mode())
        self.add_mode(self.detailed_display_mode())
        logger.info("Finished adding DrinkMenuView modes")

    def list_display_mode(self):
        self.drink_list_view = ListDrinkDisplayMode()
        return self.drink_list_view

    def detailed_display_mode(self):
        self.detailed_display = DetailedDrinkDisplayMode()
        # temp_layout = QVBoxLayout()
        # temp_layout.addWidget(self.detailed_display)
        # temp_widget = QWidget()
        # temp_widget.setLayout(temp_layout)
        return self.detailed_display

    def get_and_display_detailed_by_name(self, cocktail_name: str):
        drink_recipe = CocktailMachine.get_cocktail_recipe_by_name(cocktail_name)
        self.detailed_display.set_new_drink(cocktail=drink_recipe)
        self.inner_navigate(
            DrinkMenuModes.DISPLAY_DETAILED,
            new_title=" ".join(
                cocktail_name.split("_")).capitalize())

    def get_and_display_drinks_by_base(self, base_alcohol: str):
        all_drinks_json_list = CocktailMachine.get_cocktail_recipes_by_base(base_alcohol)
        selected_drinks_cards = []
        default_icon = icon_dict["cocktail"]
        for cocktail_name, cocktail_data in all_drinks_json_list.items():
            print(cocktail_name)
            potential_icon = icon_dict.get(cocktail_name)
            icon_path = potential_icon if potential_icon else default_icon
            cocktail_card = BaseAlcoholDrinkCard(
                title=cocktail_name,
                description=cocktail_data.summary,
                icon_path=icon_path,
                on_click=lambda x=cocktail_name: self.get_and_display_detailed_by_name(x)
            )
            selected_drinks_cards.append(cocktail_card)

        self.update_drink_list_and_show_display_mode(
            new_title=f"Base Alcohol - {base_alcohol.capitalize()}", drink_card_list=selected_drinks_cards)

    def get_and_display_drinks_by_popularity(self):
        drinks_sorted_by_popularity = CocktailMachine.get_most_popular_available_cocktails()
        selected_drink_cards = []
        for drink in drinks_sorted_by_popularity:
            selected_drink_cards.append(DrinkCard())
        self.update_drink_list_and_show_display_mode(
            f"Drinks by popularity", drink_card_list=selected_drink_cards)

    def update_drink_list_and_show_display_mode(
            self, new_title: str, drink_card_list: List[DrinkCard]):
        self.drink_list_view.set_items(drink_card_list)
        self.inner_navigate(DrinkMenuModes.DISPLAY_LIST, new_title=new_title)

    def inner_navigate(self, target_page: DrinkMenuModes, new_title: str):
        origin_page_index = self.sub_menu_layout.currentIndex()
        self.sub_menu_layout.setCurrentIndex(target_page.value)
        self.subheader.add_navigater(
            lambda: self.sub_menu_layout.setCurrentIndex(origin_page_index))
        self.subheader.update_header(title=new_title)
