

from typing import Callable
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout

from .Labels import CenterQLabel


class DrinkCard(QFrame):
    def __init__(
        self, title: str, icon_path: str, on_click: Callable
    ):
        super(DrinkCard, self).__init__()
        self._setup_drink_card(title, icon_path, on_click)

    def _setup_drink_card(self, title, icon_path, on_click):
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.on_click = on_click

        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setFixedSize(QSize(290, 340))

        self.add_title(title)
        self.add_icon(icon_path)

    def add_title(self, title):
        title = " ".join(title.split("_"))
        self.title_label = CenterQLabel(title)
        self.main_layout.addWidget(self.title_label)
        self.title_label.setMinimumHeight(65)
        self.title_label.setMaximumHeight(90)
        self.title_label.setContentsMargins(10, 15, 10, 15)
        font = self.title_label.font()
        font.setCapitalization(QFont.Capitalization.Capitalize)
        font.setPointSize(18)
        self.title_label.setFont(font)

    def add_icon(self, icon_path: str):
        icon_label = CenterQLabel()
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(100, 100)
        icon_label.setPixmap(pixmap)
        self.main_layout.addWidget(icon_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"CLICKED ON {self.__class__} - {self.title_label.text()}")
            self.on_click()
