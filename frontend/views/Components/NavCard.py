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


class NavCard(QPushButton):
  def __init__(self, text: str, on_clicked: Callable, icon_path: str = None):
    super(NavCard, self).__init__(text=(" " + text))
    if icon_path:
      icon = QIcon(icon_path)
      self.setIcon(icon)
      self.setIconSize(icon.actualSize(QSize(64,64)))
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
    shadow.setOffset(3,3)
    self.setGraphicsEffect(shadow)