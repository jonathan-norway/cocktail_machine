from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from typing import Callable
from GuiConstants import color_palette, GuiViews

class MainMenuReturnButton(QPushButton):
    def __init__(self, navigate_func: Callable):
        return_icon = QIcon("icons/return.png")
        return_icon.actualSize(QSize(36, 36))
        super(MainMenuReturnButton, self).__init__(icon=return_icon)
        self.setFixedSize(130, 30)
        self.clicked.connect(lambda: navigate_func(GuiViews.MAIN_MENU))
