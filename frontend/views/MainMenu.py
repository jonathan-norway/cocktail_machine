from PyQt6.QtWidgets import QWidget, QHBoxLayout,QLabel,QFrame, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import QSize
import sys
import os
from pathlib import Path
#sys.path.append(str(Path(__file__).parent.parent.resolve()) + "/GuiConstants.py")
from GuiConstants import color_palette, GuiViews
from typing import Callable
from .Components import NavCard
current_directory = os.path.dirname(os.path.dirname(__file__))

class MainView(QWidget):
  def __init__(self, navigate_to: Callable):
    super(MainView, self).__init__()
    vertical_layout = QVBoxLayout()
    
    
    horizontal_layout_top = QHBoxLayout()
    horizontal_layout_top.addWidget(NavCard("Drink Menu", lambda: navigate_to(GuiViews.DRINK_MENU), current_directory + "/icons/cocktail.png"))
    horizontal_layout_top.addWidget(NavCard("Custom Drink", lambda: navigate_to(GuiViews.CUSTOM_DRINK), current_directory + "/icons/bottles.png"))
    
    horizontal_layout_bottom = QHBoxLayout()
    horizontal_layout_bottom.addWidget(NavCard("Shots", lambda: navigate_to(GuiViews.SHOTS), current_directory + "/icons/shot.png"))
    horizontal_layout_bottom.addWidget(NavCard("Utils", lambda: navigate_to(GuiViews.UTILS), current_directory + "/icons/tools.png"))
    
    vertical_layout.addLayout(horizontal_layout_top)
    vertical_layout.addLayout(horizontal_layout_bottom)
    self.setLayout(vertical_layout)
  
  