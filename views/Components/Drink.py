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
from Components import CenterQLabel


class Drink(QWidget):
    def __init__(self):
        super(Drink, self).__init__()
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.add_title()
        self.add_icon()
        self.add_description()
        #self.add_indicators() for ex. sweetness?
        self.add_show_ingredients_button()
        self.add_run_button()
    
    def add_title(self):
        title_label = CenterQLabel("Cosmopolitan")
        self.main_layout.addWidget(title_label)
        
    def add_icon(self):
        icon_label = CenterQLabel()
        pixmap = QPixmap("/icons/cocktail.png")
        pixmap = pixmap.scaled(32,32)
        icon_label.setPixmap(pixmap)
        self.main_layout.addWidget(icon_label)
        
    def add_description(self, description: str):
        description_label = CenterQLabel(description if len(description) < 60 else description[:60])
        description_label.setWordWrap(True)
        self.main_layout.addWidget(description_label)
        
    def add_show_ingredients_button(self):
        show_ingredients_button = DrinkButton("Show ingredients")
        show_ingredients_button.clicked.connect()
        self.main_layout.addWidget(show_ingredients_button)
    
    def add_run_button(self):
        run_button = DrinkButton("Make me a drink!")
        run_button.clicked.connect(lambda: print("REQUESTING A DRINK"))
        self.main_layout.addWidget(run_button)
        
class DrinkButton(QPushButton):
    def __init__(self):
        super(DrinkButton, self).__init__()
