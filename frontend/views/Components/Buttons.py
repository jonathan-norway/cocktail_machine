import os
from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QLabel
from .Labels import CenterQLabel

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class PreviousButton(QPushButton):
    def __init__(self):
        return_icon = QIcon(current_directory + "/icons/return.png")
        return_icon.actualSize(QSize(36, 36))
        super(PreviousButton, self).__init__(icon=return_icon)
        self.navigation_history: list = []
        self.setFixedSize(130, 30)
        button_size_policy = self.sizePolicy()
        button_size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(button_size_policy)
        self.setVisible(False)
        self.setEnabled(False)
        self.clicked.connect(self._go_back)

    def _go_back(self):
        navigation_func = self.navigation_history.pop()
        navigation_func()
        if not (self.navigation_history):
            # self.setVisible(False)
            # self.setEnabled(False)
            self.setHidden(True)

    def update_nav(self, navigate_func: Callable):
        self.navigation_history.append(navigate_func)
        self.setVisible(True)
        self.setEnabled(True)

    def reset(self):
        self.navigation_history.clear()
        self.setEnabled(False)
        self.setVisible(False)

    def paintEvent(self, event):
        super().paintEvent(event)
        self.setGraphicsEffect(None)


class MakeMeADrinkButton(QFrame):
    def __init__(self, on_click: Callable):
        super(MakeMeADrinkButton, self).__init__()

        self.on_click = on_click
        self.main_setup()

    def main_setup(self):
        self.setLayout(QHBoxLayout())
        button_label = QLabel("Make Me A Drink!")
        button_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_label.setFixedHeight(35)
        button_label.setStyleSheet(
            "background-color: #0095ff; color: #fff; border-radius: 3px; font-size: 20px;font-weight: 500;line-height: 1.15385;")
        self.layout().addWidget(button_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("CLICKED ON MAKE-ME-A-DRINK")
            res = self.on_click()
            print(f"{res=}")
