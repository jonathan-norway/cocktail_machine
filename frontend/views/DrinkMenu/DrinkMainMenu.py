from enum import Enum, auto
from pathlib import Path
from typing import Callable

from frontend.GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from backend import CocktailMachine

from ..Components import (DetailedDrinkView, DrinkCard, DrinkList, MainMenu,
                          MenuModeCard, ModeMenuLayout, SecondHeader, Card, CardList)


class DrinkMenuModes(Enum):
    MAIN = 0
    BASE_ALCOHOL = auto()
    POPULARITY = auto()
    MOOD = auto()
    DISPLAY_LIST = auto()
    DISPLAY_DETAILED = auto()


import os

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class DrinkMenuView(MainMenu):
    def __init__(self):
        super(DrinkMenuView, self).__init__(title="Drinks")
        self.add_all_modes()

    def add_all_modes(self):
        self.add_mode(self.modes_menu())
        self.add_mode(self.base_alcohol_mode())
        self.add_mode(self.base_alcohol_mode())
        self.add_mode(self.base_alcohol_mode())
        self.add_mode(self.list_display_mode())
        self.add_mode(self.detailed_display_mode())

    def list_display_mode(self):
        v_layout = QVBoxLayout()
        self.drink_list_view = DrinkList()
        v_layout.addWidget(self.drink_list_view)
        v_layout_widget = QWidget()
        v_layout_widget.setLayout(v_layout)
        return v_layout_widget

    def detailed_display_mode(self):
        self.detailed_display = DetailedDrinkView()
        return self.detailed_display

    def modes_menu(self):
        layout = ModeMenuLayout()
        layout.addWidget(
            MenuModeCard(
                title="Base Alcohol",
                icon_path=current_directory + "/icons/bottles.png",
                description="Select a drink based on a specific base alcohol, or try a new one!",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.BASE_ALCOHOL, "Base Alcohol"),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Popularity",
                icon_path=current_directory + "/icons/popularity.png",
                description="Select a drink based on popularity. You cannot go wrong with a fan favorite!",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.POPULARITY, "Popularity"),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Mood",
                icon_path=current_directory + "/icons/season.png",
                description="Select a drink based on your mood, season, or planet orientation.",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.MOOD, "Mood"),
            )
        )
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_and_display_detailed_by_name(self, cocktail_name: str):
        drink_recipe = CocktailMachine.get_cocktail_recipe_by_name(cocktail_name)
        self.detailed_display.set_new_drink(cocktail=drink_recipe)
        self.inner_navigate(DrinkMenuModes.DISPLAY_DETAILED, new_title=cocktail_name.capitalize())

    def get_and_display_drinks_by_base(self, base_alcohol: str):
        all_drinks_json_list = CocktailMachine.get_cocktail_recipes_by_base(base_alcohol)
        selected_drinks_cards = []
        default_icon = current_directory + "/icons/cocktail.png"
        for cocktail_name, cocktail_data in all_drinks_json_list.items():
            potential_icon = current_directory + \
                f"/icons/drinks/{'-'.join(cocktail_name.split())}.png"
            icon_path = potential_icon if Path(potential_icon).exists() else default_icon
            cocktail_card = DrinkCard(
                title=cocktail_name,
                description=cocktail_data.summary,
                icon_path=icon_path,
                on_click=lambda x=cocktail_name: self.get_and_display_detailed_by_name(x)
            )
            selected_drinks_cards.append(cocktail_card)

        self.update_drink_list_and_show_display_mode(
            new_title=f"Base Alcohol - {base_alcohol.capitalize()}", drink_card_list=selected_drinks_cards)

    def update_drink_list_and_show_display_mode(self, new_title: str, drink_card_list: list):
        self.drink_list_view.set_items(drink_card_list)
        self.inner_navigate(DrinkMenuModes.DISPLAY_LIST, new_title=new_title)

    def inner_navigate(self, target_page: DrinkMenuModes, new_title: str):
        origin_page_index = self.sub_menu_layout.currentIndex()
        self.sub_menu_layout.setCurrentIndex(target_page.value)
        self.subheader.add_navigater(
            lambda: self.sub_menu_layout.setCurrentIndex(origin_page_index))
        self.subheader.update_header(title=new_title)

    def base_alcohol_mode(self):
        self.card_list = CardList()
        for base_alcohol in base_alcohols:
            self.card_list.add_card(
                Card(
                    title=base_alcohol["name"],
                    description=base_alcohol["description"],
                    icon_path=base_alcohol["icon"],
                    on_click=lambda name=base_alcohol["name"]: self.get_and_display_drinks_by_base(
                        name),
                )
            )
        return self.card_list
