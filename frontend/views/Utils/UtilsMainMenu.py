import os
from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..Components import MainMenu, MenuModeCard, ModeMenuLayout, SecondHeader

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class UtilsModeMenu(Enum):
  MAIN = 0
  UPDATE_INGREDIENTS = auto()
  UPDATE_ALCOHOLS = auto()
  UPDATE_DARKMODE = auto()
  
class UtilsMain(MainMenu):
  def __init__(self):
    super(UtilsMain,self).__init__("Utilities")
    self.add_mode(self.modes_menu())
    
  def modes_menu(self):
    layout = ModeMenuLayout()
    layout.addWidget(MenuModeCard(
      title="Update Ingredients",
      icon_path=current_directory + "/icons/shots/standard_shot.png",
      description=r"",
      on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_INGREDIENTS)
    ))
    
    layout.addWidget(MenuModeCard(
      title="Update alcohols",
      icon_path=current_directory +"/icons/shots/mixed_shot.png",
      description="",
      on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_ALCOHOLS)
    ))
    
    layout.addWidget(MenuModeCard(
      title="Set darkmode",
      icon_path=current_directory +"/icons/shots/roulette.png",
      description="Dare to take a random one?",
      on_click=lambda: self.inner_navigate(UtilsModeMenu.UPDATE_DARKMODE)
    ))
    widget = QWidget()
    widget.setLayout(layout)
    return widget
  
  def inner_navigate(self, to: UtilsModeMenu):
    self.sub_menu_layout.setCurrentIndex(to.value)
    self.subheader.previous_button.update_nav(lambda: self.sub_menu_layout.setCurrentIndex(0))
    print(to.name)