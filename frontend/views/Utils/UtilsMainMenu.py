import os
from enum import Enum, auto
from typing import Callable


from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..Components import MainMenu, Card, ModeMenuLayout, SecondHeader, InventoryTable, Card, CardList
from .PumpTable import PumpTable
from .CalibrationTool import CalibrationTool
import subprocess
import platform

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class UtilsModeMenu(Enum):
    MAIN = 0
    UPDATE_INGREDIENTS = auto()
    UPDATE_ALCOHOLS = auto()
    UPDATE_COLOR_PALETTE = auto()
    CALIBRATION_TOOL = auto()
    TEST_PUMP_MODE = auto()


class UtilsMain(MainMenu):
    def __init__(self):
        super(UtilsMain, self).__init__("Utilities")
        self.add_mode(self.modes_menu())
        self.add_mode(self.update_ingredients_mode())
        self.add_mode(self.update_alcohols_mode())
        self.add_mode(self.update_color_palette_mode())
        self.add_mode(self.calibration_tool_mode())
        self.add_mode(self.test_pump_mode())
        self.add_mode(self.pull_latest())

    def update_color_palette_mode(self):
        return QWidget()

    def calibration_tool_mode(self):
        return CalibrationTool()

    def test_pump_mode(self):
        return QWidget()

    def pull_latest(self):
        return QWidget()

    def modes_menu(self):
        widget = CardList()
        widget.add_card(Card(
            title="Update<br>Ingredients",
            icon_path=current_directory + "/icons/utils/fridge.png",
            description=r"",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_INGREDIENTS)
        ))

        widget.add_card(Card(
            title="Update Pumps",
            icon_path=current_directory + "/icons/utils/measuring-cup.png",
            description="",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_ALCOHOLS)
        ))

        widget.add_card(Card(
            title="Update Color Palette",
            icon_path=current_directory + "/icons/utils/color-circle.png",
            description="Change color scheme",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_COLOR_PALETTE)
        ))

        widget.add_card(Card(
            title="Calibration Tool",
            icon_path=current_directory + "/icons/utils/level.png",
            description="",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.CALIBRATION_TOOL)
        ))

        widget.add_card(Card(
            title="Test Pumps",
            icon_path=current_directory + "/icons/utils/pump.png",
            description="",
            on_click=lambda: self.inner_navigate(UtilsModeMenu.TEST_PUMP_MODE)
        ))

        widget.add_card(Card(
            title="Update Software",
            icon_path=current_directory + "/icons/utils/github.png",
            description="",
            on_click=lambda: self.trigger_software_update()
        ))
        return widget

    def trigger_software_update(self):
        print("PULL LATEST FROM GITHUB NOW!!")
        if platform.system() != "Windows":
            print("ACTUALLY UPDATING!!")
            command_to_run = "/home/jonathan-pi/startup.sh"
            subprocess.Popen(command_to_run, shell=True)

    def inner_navigate(self, to: UtilsModeMenu):
        previous_index = self.sub_menu_layout.currentIndex()
        self.subheader.add_navigater(
            lambda: self.sub_menu_layout.setCurrentIndex(
                previous_index))
        self.sub_menu_layout.setCurrentIndex(to.value)

    def update_ingredients_mode(self):
        return InventoryTable()

    def update_alcohols_mode(self):
        return PumpTable()
