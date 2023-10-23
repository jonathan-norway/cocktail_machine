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
    QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtCore import Qt, QSize
from GuiConstants import color_palette, GuiViews
from typing import Callable
from enum import Enum, auto


class DrinkMenuModes(Enum):
    MAIN = 0
    BASE_ALCOHOL = auto()
    POPULARITY = auto()
    MOOD = auto()


class DrinkMenuView(QWidget):
    def __init__(self, navigate_func: Callable):
        super(DrinkMenuView, self).__init__()
        self.setFixedHeight(500)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)

        subheader_widget = self.create_subheader(lambda: self.inner_navigate(DrinkMenuModes.MAIN))
        self.sub_menu_layout = QStackedLayout()
        self.sub_menu_layout.addWidget(self.menu_modes_menu())
        self.sub_menu_layout.addWidget(self.base_alcohol_mode())
        sub_menu_widget = QWidget()
        sub_menu_widget.setFixedHeight(450)
        sub_menu_widget.setLayout(self.sub_menu_layout)
        main_layout.addWidget(subheader_widget)
        main_layout.addWidget(sub_menu_widget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3,3)
        self.setGraphicsEffect(shadow)


    def inner_navigate(self, to: DrinkMenuModes):
        self.sub_menu_layout.setCurrentIndex(to.value)
        print(to.name)
        
        
    def base_alcohol_mode(self):
        # Could be Vodka(6), Gin(5), Rum(3), Whiskey(3), Tequila(1)
        self.card_list = CardList()
        self.card_list.add_card(Card(title="Vodka", description="Smooth and tasteless alcohol. The most popular in drinks all over the world. Usually made from potato or grains.", icon_path="icons/cocktail.png", on_click=lambda: print("PRESSED VODKA")))
        return self.card_list

    def menu_modes_menu(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout.setSpacing(20)
        layout.addWidget(
            MenuModeCard(
                title="Base Alcohol",
                icon_path="icons/bottles.png",
                description="Select a drink based on a specific base alcohol, or try a new one!",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.BASE_ALCOHOL),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Popularity",
                icon_path="icons/popularity.png",
                description="Select a drink based on popularity. You cannot go wrong with a fan favorite!",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.POPULARITY),
            )
        )
        layout.addWidget(
            MenuModeCard(
                title="Mood",
                icon_path="icons/season.png",
                description="Select a drink based on your mood, season, or planet orientation.",
                on_click=lambda: self.inner_navigate(DrinkMenuModes.MOOD),
            )
        )
        widget = QWidget()
        widget.setLayout(layout)
        self.setFixedHeight(450)
        return widget

    def create_subheader(self, navigate_func: Callable):
        subheader_layout = QHBoxLayout()
        subheader_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.subheader_return_arrow = MainMenuReturnButton(lambda x: navigate_func())

        subheader_icon_label = QLabel()
        subheader_pixmap = QPixmap("icons/cocktail.png")
        subheader_pixmap = subheader_pixmap.scaled(
            QSize(36, 36),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        subheader_icon_label.setPixmap(subheader_pixmap)

        font = QFont()
        font.setPointSize(26)
        self.setFixedHeight(260)
        self.setFont(font)
        subheader_text = QLabel("Drink Menu")

        subheader_spacing_item = QSpacerItem(
            150, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        main_label_layout = QHBoxLayout()
        main_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_label_layout.addWidget(subheader_icon_label)
        main_label_layout.addWidget(subheader_text)
        main_label_widget = QWidget()
        main_label_widget.setLayout(main_label_layout)
        subheader_layout.addSpacerItem(QSpacerItem(15,5))
        subheader_layout.addWidget(
            self.subheader_return_arrow, Qt.AlignmentFlag.AlignLeft
        )
        subheader_layout.addWidget(main_label_widget, Qt.AlignmentFlag.AlignCenter)
        subheader_layout.addItem(subheader_spacing_item)
        # subheader_layout.addWidget(subheader_icon_label, Qt.AlignmentFlag.AlignCenter)
        # subheader_layout.addWidget(subheader_text, Qt.AlignmentFlag.AlignCenter)
        subheader_widget = QWidget()
        subheader_widget.setLayout(subheader_layout)
        return subheader_widget


class MenuModeCard(QFrame):
    def __init__(
        self,
        title: str,
        on_click: Callable,
        icon_path: str = None,
        description: str = "",
    ):
        super(MenuModeCard, self).__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        self.on_click = on_click
        
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label)
        
        
        icon_label = QLabel()
        #icon_label.setFixedHeight(60)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(
            QSize(60, 60),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)

        description_label = QLabel(description)
        description_font = QFont()
        description_font.setPointSize(16)
        description_label.setFont(description_font)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        description_label.setFixedHeight(80)
        layout.addWidget(description_label)
        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setFixedSize(QSize(300, 340))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()


class MainMenuReturnButton(QPushButton):
    def __init__(self, navigate_func: Callable):
        return_icon = QIcon("icons/return.png")
        return_icon.actualSize(QSize(36, 36))
        super(MainMenuReturnButton, self).__init__(icon=return_icon)
        self.setFixedSize(130, 30)
        self.clicked.connect(lambda: navigate_func(GuiViews.MAIN_MENU))


class Card(QFrame):
    def __init__(self, icon_path: str, title: str, description: str, on_click: Callable):
        super(Card, self).__init__()
        self.on_click = on_click
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(QSize(36,36), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label = QLabel()
        icon_label.setPixmap(icon_pixmap)
        #icon_label.setFixedSize(QSize(150,150))
        self.main_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        self.main_layout.addWidget(title_label)
        
        description_label = QLabel(description)
        description_label.setWordWrap(True)
        self.main_layout.addWidget(description_label)
        #self.setFixedSize(QSize(150,100))
        #self.setStyleSheet("border: 2px solid red;")
        self.setFrameStyle(1)
        self.setLineWidth(1)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()

class CardList(QWidget):
    MAX_PR_ROW = 3
    def __init__(self):
        super(CardList, self).__init__()
        self.main_layout = QVBoxLayout()
        self.item_layouts = []
        self.item_layouts.append(self.get_new_layout())
        self.setLayout(self.main_layout)
        #self.setFixedSize(QSize(600,450))
        #self.setStyleSheet("background-color: red")
    
    def add_card(self, card: Card):
        current_layout = self.item_layouts[-1]
        if current_layout.count() >= CardList.MAX_PR_ROW:
            print("added")
            current_layout = self.get_new_layout()
            self.item_layouts.append(current_layout)
        current_layout.addWidget(card)
            
    def get_new_layout(self):
        new_layout = QHBoxLayout()
        self.main_layout.addLayout(new_layout)
        new_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        return new_layout
    
