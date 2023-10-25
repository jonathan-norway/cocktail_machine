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
from ..Components import SecondHeader, ModeMenuLayout, MenuModeCard

class ShotModeMenu(Enum):
    MAIN = 0
    STANDARD = auto()
    MIXED = auto()
    ROULETTE = auto()

class ShotsMainMenu(QWidget):
  def __init__(self):
    super(ShotsMainMenu, self).__init__()
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(0,0,0,0)
    main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
    self.setLayout(main_layout)
    self.subheader = SecondHeader()
  
    self.sub_menu_layout = QStackedLayout()
    self.sub_menu_layout.addWidget(self.modes_menu())
    #self.sub_menu_layout.addWidget(self.random_mode())
    sub_menu_widget = QWidget()
    sub_menu_widget.setLayout(self.sub_menu_layout)
    main_layout.addWidget(self.subheader)
    main_layout.addWidget(sub_menu_widget)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(10)
    shadow.setColor(QColor("#555555"))
    shadow.setOffset(3, 3)
    self.setGraphicsEffect(shadow)
    
  def modes_menu(self):
    layout = ModeMenuLayout()
    layout.addWidget(MenuModeCard(
      title="Standard",
      icon_path="icons/shots/standard_shot.png",
      description=r"You miss 100% of the shots you don't take..",
      on_click=lambda: self.inner_navigate(ShotModeMenu.STANDARD)
    ))
    
    layout.addWidget(MenuModeCard(
      title="Mixed",
      icon_path="icons/shots/mixed_shot.png",
      description="Couldn't decide between a drink or a shot? Try something in the middle",
      on_click=lambda: self.inner_navigate(ShotModeMenu.MIXED)
    ))
    
    layout.addWidget(MenuModeCard(
      title="Roulette",
      icon_path="icons/shots/roulette.png",
      description="Dare to take a random one?",
      on_click=lambda: self.inner_navigate(ShotModeMenu.ROULETTE)
    ))
    widget = QWidget()
    widget.setLayout(layout)
    return widget
    
  def inner_navigate(self, to: ShotModeMenu):
      self.sub_menu_layout.setCurrentIndex(to.value)
      self.subheader.previous_button.update_nav(lambda: self.sub_menu_layout.setCurrentIndex(0))
      print(to.name)
  