
from typing import Callable, Optional

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QPushButton


class NavCard(QPushButton):
    def __init__(self, text: str, on_clicked: Callable, icon_path: str = None):
        super(NavCard, self).__init__(text=(" " + text))
        self.setup_nav_card(text, on_clicked, icon_path)

    def setup_nav_card(self, text: str, on_clicked: Callable[[
                       None], None], icon_path: Optional[str] = None) -> None:
        if icon_path:
            self.set_icon(icon_path)
        self.set_font()
        self.setFixedHeight(210)
        self.clicked.connect(on_clicked)
        self.setStyleSheet("""
      QPushButton {
        border-radius: 5px;
        border: 2px solid black;
      }
        """)
        self.set_shadow()

    def set_icon(self, icon_path: str):
        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconSize(icon.actualSize(QSize(64, 64)))

    def set_font(self):
        font = self.font()
        font.setPointSize(26)
        font.setCapitalization(QFont.Capitalization.AllUppercase)
        self.setFont(font)

    def set_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)
