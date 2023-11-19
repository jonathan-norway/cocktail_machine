from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from .Headers import SecondHeader
from .ModeMenu import ModeMenuLayout


class MainMenu(QWidget):
    def __init__(self, title: str):
        super(MainMenu, self).__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)
        self.subheader = SecondHeader(title)

        self.sub_menu_layout = QStackedLayout()
        sub_menu_widget = QWidget()
        sub_menu_widget.setLayout(self.sub_menu_layout)
        main_layout.addWidget(self.subheader)
        main_layout.addWidget(sub_menu_widget)
        self.set_shadow()

    def set_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)

    def add_mode(self, mode: QWidget):
        self.sub_menu_layout.addWidget(mode)
