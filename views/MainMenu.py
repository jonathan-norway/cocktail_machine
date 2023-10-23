from PyQt6.QtWidgets import QWidget, QHBoxLayout,QLabel,QFrame, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPainter
from PyQt6.QtCore import QSize
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()) + "/GuiConstants.py")
print(sys.path)
from GuiConstants import color_palette, GuiViews
from typing import Callable


class MainView(QWidget):
  def __init__(self, navigate_to: Callable):
    super(MainView, self).__init__()
    vertical_layout = QVBoxLayout()
    
    
    horizontal_layout_top = QHBoxLayout()
    horizontal_layout_top.addWidget(NavButton("Drink Menu", lambda: navigate_to(GuiViews.DRINK_MENU), "icons/cocktail.png"))
    horizontal_layout_top.addWidget(NavButton("Custom Drink", lambda: navigate_to(GuiViews.CUSTOM_DRINK), "icons/bottles.png"))
    
    horizontal_layout_bottom = QHBoxLayout()
    horizontal_layout_bottom.addWidget(NavButton("Shots", lambda: navigate_to(GuiViews.SHOTS), "icons/shot.png"))
    horizontal_layout_bottom.addWidget(NavButton("Utils", lambda: navigate_to(GuiViews.UTILS), "icons/tools.png"))
    
    vertical_layout.addLayout(horizontal_layout_top)
    vertical_layout.addLayout(horizontal_layout_bottom)
    self.setLayout(vertical_layout)
    
    
  
    
class NavButton(QPushButton):
  def __init__(self, text: str, on_clicked: Callable, icon_path: str = None):
    super(NavButton, self).__init__(text=(" " + text))
    if icon_path:
      icon = QIcon(icon_path)
      self.setIcon(icon)
      self.setIconSize(icon.actualSize(QSize(64,64)))
    font = QFont()
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
  
  