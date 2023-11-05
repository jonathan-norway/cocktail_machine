from enum import Enum, auto
from pathlib import Path
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from backend import CocktailMachine

from frontend.views.Components import (DetailedDrinkView, DrinkCard, DrinkList, MainMenu,
                                       MenuModeCard, ModeMenuLayout, SecondHeader)


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
        super(DrinkMenuView, self).__init__("Drinks")
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
                on_click=lambda: self.inner_navigate(DrinkMenuModes.BASE_ALCOHOL),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Popularity",
                icon_path=current_directory + "/icons/popularity.png",
                description="Select a drink based on popularity. You cannot go wrong with a fan favorite!",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.POPULARITY),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Mood",
                icon_path=current_directory + "/icons/season.png",
                description="Select a drink based on your mood, season, or planet orientation.",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.MOOD),
            )
        )
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def get_and_display_detailed_by_name(self, cocktail_name: str):
        drink_recipe = CocktailMachine.get_cocktail_recipe_by_name(cocktail_name)
        self.detailed_display.set_new_drink(cocktail=drink_recipe)
        self.inner_navigate(DrinkMenuModes.DISPLAY_DETAILED)

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

        self.update_drink_list_and_show_display_mode(selected_drinks_cards)

    def update_drink_list_and_show_display_mode(self, drink_card_list: list):
        self.drink_list_view.set_items(drink_card_list)
        self.inner_navigate(DrinkMenuModes.DISPLAY_LIST)

    def inner_navigate(self, target_page: DrinkMenuModes):
        origin_page_index = self.sub_menu_layout.currentIndex()
        self.sub_menu_layout.setCurrentIndex(target_page.value)
        self.subheader.previous_button.update_nav(
            lambda: self.sub_menu_layout.setCurrentIndex(origin_page_index))

    def base_alcohol_mode(self):
        self.card_list = CardList()
        for base_alcohol in base_alcohols:
            self.card_list.add_card(
                Card(
                    title=base_alcohol["name"],
                    description=base_alcohol["description"],
                    icon_path=base_alcohol["icon"],
                    on_click=lambda _, name=base_alcohol["name"]: self.get_and_display_drinks_by_base(
                        name),
                )
            )
        return self.card_list


class Card(QFrame):
    def __init__(
        self, icon_path: str, title: str, description: str, on_click: Callable
    ):
        super(Card, self).__init__()
        self.on_click = lambda: on_click(title)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        title_label = QLabel(title)
        title_font = title_label.font()
        title_font.setCapitalization(QFont.Capitalization.Capitalize)
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(title_label)

        icon_pixmap = QPixmap(icon_path)
        self.icon_pixmap = icon_pixmap.scaled(
            QSize(45, 45),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label = QLabel()
        icon_label.setPixmap(self.icon_pixmap)
        # icon_label.setFixedSize(QSize(150,150))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(icon_label)

        description_label = QLabel(description if len(description) < 100 else description[0:100])
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        description_font = description_label.font()
        description_font.setPointSize(14)
        description_label.setFont(description_font)
        self.main_layout.addWidget(description_label)
        self.setFixedSize(QSize(275, 200))
        # self.setStyleSheet("border: 2px solid red;")
        self.setFrameStyle(1)
        self.setLineWidth(1)
        # self.setContentsMargins(5,10,5,0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()


class CardList(QWidget):
    MAX_PR_ROW = 3
    Y_SPACING = 15
    X_SPACING = 15

    def __init__(self):
        super(CardList, self).__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setSpacing(CardList.Y_SPACING)
        self.item_layouts = []
        self.item_layouts.append(self.get_new_layout())
        self.setLayout(self.main_layout)
        # self.setContentsMargins(0,0,0,0)
        # self.setFixedSize(QSize(600,450))
        # self.setStyleSheet("border: 2px solid red")

    def add_card(self, card: Card):
        current_layout = self.item_layouts[-1]
        if current_layout.count() >= CardList.MAX_PR_ROW:
            print("added")
            current_layout = self.get_new_layout()
            self.item_layouts.append(current_layout)
        current_layout.addWidget(card)

    def get_new_layout(self):
        new_layout = QHBoxLayout()
        self.main_layout.addLayout(new_layout)
        new_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        new_layout.setSpacing(CardList.X_SPACING)
        return new_layout
