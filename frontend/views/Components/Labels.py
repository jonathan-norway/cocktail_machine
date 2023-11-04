from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QStackedLayout,
    QFrame,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QSize
from GuiConstants import color_palette, GuiViews, base_alcohols
from typing import Callable
from enum import Enum, auto

class CenterQLabel(QLabel):
    def __init__(self, title: str=None):
        super(CenterQLabel, self).__init__(text=title)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setContentsMargins(0,0,0,0)
