from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class CustomDrinkMenu(QWidget):
  def __init__(self):
    super(CustomDrinkMenu, self).__init__()
    layout = QVBoxLayout()
    layout.addWidget(QLabel("In construction..."))
    self.setLayout(layout)