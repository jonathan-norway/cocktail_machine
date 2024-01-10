import os
from enum import Enum, auto
from typing import Callable

from frontend.GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton, QFrame, QHBoxLayout, QLabel, QWidget
from .Labels import CenterQLabel

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
from frontend import GuiConstants


class MainMenuReturnButton(QWidget):
    def __init__(self, navigate_func: Callable):
        super(MainMenuReturnButton, self).__init__()
        return_pixmap = QPixmap(current_directory + "/icons/house.png")
        return_pixmap = return_pixmap.scaled(
            QSize(
                55,
                55),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        sizePolicy = self.sizePolicy()
        sizePolicy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(sizePolicy)
        self.return_label = QLabel()
        self.return_label.setPixmap(return_pixmap)
        self.return_label.setFixedSize(60, 60)
        self.navigate_func = navigate_func
        default_layout = QHBoxLayout()
        default_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        default_layout.addWidget(self.return_label)
        self.setLayout(default_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.navigate_func(GuiConstants.GuiViews.MAIN_MENU)


class PreviousButton(QPushButton):
    def __init__(self):
        return_icon = QIcon(current_directory + "/icons/return.png")
        # return_icon.actualSize(QSize(50, 36))
        super(PreviousButton, self).__init__(icon=return_icon)
        self.navigation_history: list[(Callable, Callable)] = []
        button_size_policy = self.sizePolicy()
        button_size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(button_size_policy)
        self.setFixedSize(QSize(75, 35))
        self.setVisible(False)
        self.setEnabled(False)
        self.clicked.connect(self._go_back)

    def _go_back(self):
        (navigation_func, title_func) = self.navigation_history.pop()
        navigation_func()
        title_func()
        if not (self.navigation_history):
            # self.setVisible(False)
            # self.setEnabled(False)
            self.setHidden(True)

    def update_nav(self, navigate_func: Callable, title_func: Callable):
        self.navigation_history.append((navigate_func, title_func))
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


class MainMenuReturnButton(QWidget):
    def __init__(self, navigate_func: Callable):
        super(MainMenuReturnButton, self).__init__()
        return_pixmap = QPixmap(current_directory + "/icons/house.png")
        return_pixmap = return_pixmap.scaled(
            QSize(
                55,
                55),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        sizePolicy = self.sizePolicy()
        sizePolicy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(sizePolicy)
        self.return_label = QLabel()
        self.return_label.setPixmap(return_pixmap)
        self.return_label.setFixedSize(60, 60)
        self.navigate_func = navigate_func
        default_layout = QHBoxLayout()
        default_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        default_layout.addWidget(self.return_label)
        self.setLayout(default_layout)
        self.setVisible(True)
        self.setContentsMargins(150, 0, 0, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.navigate_func(GuiConstants.GuiViews.MAIN_MENU)
