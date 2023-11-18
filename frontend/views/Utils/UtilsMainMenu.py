import os
from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..Components import MainMenu, MenuModeCard, ModeMenuLayout, SecondHeader
from .InventoryTable import InventoryTable
current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class UtilsModeMenu(Enum):
    MAIN = 0
    UPDATE_INGREDIENTS = auto()
    UPDATE_ALCOHOLS = auto()
    UPDATE_DARKMODE = auto()


class UtilsMain(MainMenu):
    def __init__(self):
        super(UtilsMain, self).__init__("Utilities")
        self.add_mode(self.modes_menu())
        self.add_mode(self.update_ingredients_mode())

    def modes_menu(self):
        layout = ModeMenuLayout()
        layout.addWidget(MenuModeCard(
            title="Update<br>Ingredients",
            icon_path=current_directory + "/icons/utils/fridge.png",
            description=r"",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_INGREDIENTS)
        ))

        layout.addWidget(MenuModeCard(
            title="Update Pumps",
            icon_path=current_directory + "/icons/utils/measuring-cup.png",
            description="",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_ALCOHOLS)
        ))

        layout.addWidget(MenuModeCard(
            title="Set darkmode",
            icon_path=current_directory + "/icons/utils/day-and-night.png",
            description="Change color scheme",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_DARKMODE)
        ))
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def inner_navigate(self, to: UtilsModeMenu):
        previous_index = self.sub_menu_layout.currentIndex()
        self.subheader.previous_button.update_nav(
            lambda: self.sub_menu_layout.setCurrentIndex(
                previous_index))
        self.sub_menu_layout.setCurrentIndex(to.value)

    def update_ingredients_mode(self):
        return InventoryTable()
