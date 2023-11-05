import os

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class CustomDrinkMenu(QWidget):
  def __init__(self):
    super(CustomDrinkMenu, self).__init__()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("In construction..."))
    self.setLayout(layout)