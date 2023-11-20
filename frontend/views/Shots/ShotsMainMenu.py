import os
from enum import Enum, auto
from typing import Callable

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..Components import MainMenu, MenuModeCard, ModeMenuLayout, SecondHeader

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class ShotModeMenu(Enum):
    MAIN = 0
    STANDARD = auto()
    MIXED = auto()
    ROULETTE = auto()


class ShotsMainMenu(MainMenu):
    def __init__(self):
        super(ShotsMainMenu, self).__init__("Shots")
        self.add_mode(self.modes_menu())

    def modes_menu(self):
        layout = ModeMenuLayout()
        layout.addWidget(MenuModeCard(
            title="Standard",
            icon_path=current_directory + "/icons/shots/standard_shot.png",
            description=r"You miss 100% of the shots you don't take..",
            on_click=lambda: self.inner_navigate(ShotModeMenu.STANDARD)
        ))

        layout.addWidget(MenuModeCard(
            title="Mixed",
            icon_path=current_directory + "/icons/shots/mixed_shot.png",
            description="Couldn't decide between a drink or a shot? Try something in the middle",
            on_click=lambda: self.inner_navigate(ShotModeMenu.MIXED)
        ))

        layout.addWidget(MenuModeCard(
            title="Roulette",
            icon_path=current_directory + "/icons/shots/roulette.png",
            description="Dare to take a random one?",
            on_click=lambda: self.inner_navigate(ShotModeMenu.ROULETTE)
        ))
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def inner_navigate(self, to: ShotModeMenu):
        self.sub_menu_layout.setCurrentIndex(to.value)
        self.subheader.previous_button.update_nav(lambda: self.sub_menu_layout.setCurrentIndex(0))
        print(to.name)
