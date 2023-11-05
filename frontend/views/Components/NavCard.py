from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)


class NavCard(QPushButton):
    def __init__(self, text: str, on_clicked: Callable, icon_path: str = None):
        super(NavCard, self).__init__(text=(" " + text))
        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconSize(icon.actualSize(QSize(64, 64)))
        font = self.font()
        font.setPointSize(22)
        font.setCapitalization(QFont.Capitalization.AllUppercase)
        self.setFont(font)
        self.setFixedHeight(260)
        self.clicked.connect(lambda: on_clicked())
        self.setStyleSheet("""
      QPushButton {
        border-radius: 5px;
        border: 2px solid black;
      }
    """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)
