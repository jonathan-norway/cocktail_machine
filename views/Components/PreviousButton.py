from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QSize
from GuiConstants import color_palette, GuiViews, base_alcohols
from typing import Callable
from enum import Enum, auto


class PreviousButton(QPushButton):
    def __init__(self):
        return_icon = QIcon("icons/return.png")
        return_icon.actualSize(QSize(36, 36))
        super(PreviousButton, self).__init__(icon=return_icon)
        self.navigation_history: list  = []
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
        #self.setVisible(False)
        #self.setEnabled(False)
        self.setHidden(True)
      
    def update_nav(self, navigate_func: Callable):
      self.navigation_history.append(navigate_func)
      self.setVisible(True)
      self.setEnabled(True)
      
    def reset(self):
      self.navigation_history.clear()
      self.setEnabled(False)
      self.setVisible(False)
