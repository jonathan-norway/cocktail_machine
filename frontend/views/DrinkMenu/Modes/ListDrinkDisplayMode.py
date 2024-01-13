from frontend.components import CardList, Card
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from frontend.GuiConstants import base_alcohols
from typing import Callable
import math
import os
from pathlib import Path
from typing import List
from frontend.icons import icon_dict
import qrcode
from PyQt5.QtCore import QObjectCleanupHandler, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QGridLayout,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from backend.cocktail_machine import CocktailMachine

from frontend.components.Drink import DrinkCard
from frontend.components.Labels import CenterQLabel
from frontend.components.Buttons import MakeMeADrinkButton, ListNavigateButton
import logging
logger = logging.getLogger(__name__)


ITEMS_TO_SHOW = 4


class ListDrinkDisplayMode(QWidget):
    def __init__(self, items: List[DrinkCard] = [], items_per_line=4, total_lines=1):
        super(ListDrinkDisplayMode, self).__init__()
        self.page = 0
        self.items_per_line = items_per_line
        self.total_lines = total_lines
        self.main_setup()
        self.set_items(items)

    def set_items(self, items: list):
        self.items = items
        while self.stacked_layout.count():
            item = self.stacked_layout.takeAt(0)
            if item:
                item.widget().deleteLater()
        self.setup_stacked_layout()

    def main_setup(self):
        main_layout = QVBoxLayout()
        self.stacked_layout = QStackedLayout()

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.previous_button = ListNavigateButton(
            icon_path=icon_dict["return"],
            on_click=self.load_previous,
        )
        # self.previous_button.clicked.connect(self.load_previous)
        self.next_button = ListNavigateButton(
            icon_path=icon_dict["next-page"],
            on_click=self.load_next,
        )
        # self.next_button.clicked.connect()
        button_layout.addWidget(self.previous_button)
        button_layout.addSpacerItem(QSpacerItem(30, 5))
        button_layout.addWidget(self.next_button)

        self.stacked_layout_widget = QWidget()
        self.stacked_layout_widget.setLayout(self.stacked_layout)
        main_layout.addWidget(self.stacked_layout_widget)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def setup_stacked_layout(self):
        stacked_layout = self.stacked_layout
        self.horizontal_layouts = [
            QHBoxLayout() for _ in range(math.ceil(len(self.items) / ITEMS_TO_SHOW))
        ]
        for index, item in enumerate(self.items):
            item.setFixedWidth(230)
            self.horizontal_layouts[index // ITEMS_TO_SHOW].addWidget(item)
        for layout in self.horizontal_layouts:
            widget = QWidget()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget.setLayout(layout)
            stacked_layout.addWidget(widget)
        # self.setLayout(main_layout)

    def load_next(self):
        print("trying to load next")
        if self.can_go_next():
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() + 1)

            if not self.can_go_next():
                self.next_button.setHidden(True)
            self.previous_button.setHidden(False)

    def load_previous(self):
        print("trying to load previous")
        if self.can_go_back():
            print("went back")
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() - 1)
            if not self.can_go_back():
                self.previous_button.setHidden(True)
            self.next_button.setHidden(False)

    def can_go_back(self) -> bool:
        return 0 < self.stacked_layout.currentIndex()

    def can_go_next(self) -> bool:
        return self.stacked_layout.count() - 1 > self.stacked_layout.currentIndex()


class BaseAlcoholDrinkCard(DrinkCard):
    def __init__(self, title: str, icon_path: str, description: str, on_click: Callable
                 ):
        super(BaseAlcoholDrinkCard, self).__init__(
            title=title, icon_path=icon_path, on_click=on_click
        )
        self._setup_base_alcohol_drink_card(description)

    def _setup_base_alcohol_drink_card(self, description: str) -> None:
        self.add_description(description)
        # self.add_indicators() for ex. sweetness/ratings/how many made?

    def add_description(self, description: str):
        description_label = CenterQLabel(
            description if len(description) < 60 else description[:60]
        )
        description_label.setWordWrap(True)
        description_label.setContentsMargins(15, 0, 15, 0)
        font = description_label.font()
        font.setPointSize(14)
        description_label.setFont(font)
        self.main_layout.addWidget(description_label)


class PopularityDrinkCard(DrinkCard):
    def __init__(self, title: str, icon_path: str, description: str, on_click: Callable
                 ):
        super(BaseAlcoholDrinkCard, self).__init__(
            title=title, icon_path=icon_path, description=description, on_click=on_click
        )
