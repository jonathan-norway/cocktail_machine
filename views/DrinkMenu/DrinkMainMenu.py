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

class DrinkMenuModes(Enum):
    MAIN = 0
    BASE_ALCOHOL = auto()
    POPULARITY = auto()
    MOOD = auto()


class DrinkMenuView(QWidget):
    def __init__(self):
        super(DrinkMenuView, self).__init__()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)
        self.subheader = SecondHeader()

      
        self.sub_menu_layout = QStackedLayout()
        self.sub_menu_layout.addWidget(self.menu_modes_menu())
        self.sub_menu_layout.addWidget(self.base_alcohol_mode())
        sub_menu_widget = QWidget()
        sub_menu_widget.setLayout(self.sub_menu_layout)
        main_layout.addWidget(self.subheader)
        main_layout.addWidget(sub_menu_widget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)
        #self.setFixedHeight(500)
    
    def menu_modes_menu(self):
        layout = ModeMenuLayout()
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
        return widget


    def inner_navigate(self, to: DrinkMenuModes):
        self.sub_menu_layout.setCurrentIndex(to.value)
        self.subheader.previous_button.update_nav(lambda: self.sub_menu_layout.setCurrentIndex(0))
        print(to.name)

    def base_alcohol_mode(self):
        self.card_list = CardList()
        for base_alcohol in base_alcohols:
            self.card_list.add_card(
                Card(
                    title=base_alcohol["name"],
                    description=base_alcohol["description"],
                    icon_path=base_alcohol["icon"],
                    on_click=lambda x: print(f"PRESSED {x}"),
                )
            )
        return self.card_list

   


class Card(QFrame):
    def __init__(
        self, icon_path: str, title: str, description: str, on_click: Callable
    ):
        super(Card, self).__init__()
        self.on_click = lambda: on_click(title)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

     

        title_label = QLabel(title)
        title_font = title_label.font()
        title_font.setCapitalization(QFont.Capitalization.Capitalize)
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(title_label)


        icon_pixmap = QPixmap(icon_path)
        self.icon_pixmap = icon_pixmap.scaled(
            QSize(45, 45),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label = QLabel()
        icon_label.setPixmap(self.icon_pixmap)
        # icon_label.setFixedSize(QSize(150,150))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(icon_label)


        description_label = QLabel(description if len(description) < 100 else description[0:100])
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        description_font = description_label.font()
        description_font.setPointSize(14)
        description_label.setFont(description_font)
        self.main_layout.addWidget(description_label)
        self.setFixedSize(QSize(275,200))
        # self.setStyleSheet("border: 2px solid red;")
        self.setFrameStyle(1)
        self.setLineWidth(1)
        #self.setContentsMargins(5,10,5,0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()


class CardList(QWidget):
    MAX_PR_ROW = 3
    Y_SPACING = 15
    X_SPACING = 15
    def __init__(self):
        super(CardList, self).__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.main_layout.setSpacing(CardList.Y_SPACING)
        self.item_layouts = []
        self.item_layouts.append(self.get_new_layout())
        self.setLayout(self.main_layout)
        #self.setContentsMargins(0,0,0,0)
        # self.setFixedSize(QSize(600,450))
        #self.setStyleSheet("border: 2px solid red")

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
        new_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        new_layout.setSpacing(CardList.X_SPACING)
        return new_layout
