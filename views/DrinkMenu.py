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


class DrinkMenuModes(Enum):
    MAIN = 0
    BASE_ALCOHOL = auto()
    POPULARITY = auto()
    MOOD = auto()


class DrinkMenuView(QWidget):
    def __init__(self):
        super(DrinkMenuView, self).__init__()
        #self.setFixedHeight(300)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)

        subheader_widget = DrinkMenuView.get_subheader(
            lambda: self.inner_navigate(DrinkMenuModes.MAIN)
        )
        self.sub_menu_layout = QStackedLayout()
        self.sub_menu_layout.addWidget(self.menu_modes_menu())
        self.sub_menu_layout.addWidget(self.base_alcohol_mode())
        sub_menu_widget = QWidget()
        sub_menu_widget.setLayout(self.sub_menu_layout)
        main_layout.addWidget(subheader_widget)
        main_layout.addWidget(sub_menu_widget)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor("#555555"))
        shadow.setOffset(3, 3)
        self.setGraphicsEffect(shadow)
        #self.setFixedHeight(500)

    def inner_navigate(self, to: DrinkMenuModes):
        self.sub_menu_layout.setCurrentIndex(to.value)
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

    def menu_modes_menu(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        return widget

    def get_subheader(navigate_func: Callable):
        subheader_layout = QHBoxLayout()
        subheader_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        subheader_return_arrow = MainMenuReturnButton(lambda x: navigate_func())

        subheader_icon_label = QLabel()
        subheader_pixmap = QPixmap("icons/cocktail.png")
        subheader_pixmap = subheader_pixmap.scaled(
            QSize(36, 36),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        subheader_icon_label.setPixmap(subheader_pixmap)

        subheader_title = QLabel("Drink Menu")
        font = subheader_title.font()
        font.setPointSize(26)
        #self.setFixedHeight(260)
        subheader_title.setFont(font)

        subheader_spacing_item = QSpacerItem(
            150, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        main_label_layout = QHBoxLayout()
        main_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignTop)
        main_label_layout.addWidget(subheader_icon_label)
        main_label_layout.addWidget(subheader_title)
        main_label_layout.setContentsMargins(0,0,0,0)
        main_label_widget = QWidget()
        main_label_widget.setLayout(main_label_layout)
        subheader_layout.addSpacerItem(QSpacerItem(15, 5))
        subheader_layout.addWidget(
            subheader_return_arrow, Qt.AlignmentFlag.AlignLeft
        )
        subheader_layout.addWidget(main_label_widget, Qt.AlignmentFlag.AlignCenter)
        subheader_layout.addItem(subheader_spacing_item)
        subheader_layout.setContentsMargins(0,0,0,0)
        subheader_layout.setSpacing(0)
        subheader_widget = QWidget()
        subheader_widget.setLayout(subheader_layout)
        subheader_widget.setContentsMargins(0,0,0,0)
        subheader_widget.setFixedHeight(50)
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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter)
        self.on_click = on_click

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_font = title_label.font()
        title_font.setPointSize(22)
        title_label.setFont(title_font)
        title_label.setContentsMargins(0,15,0,20)
        layout.addWidget(title_label)


        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(
            QSize(85, 85),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(icon_label)

        description_label = QLabel(description)
        description_font = QFont()
        description_font.setPointSize(16)
        description_label.setFont(description_font)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        description_label.setFixedHeight(100)
        description_label.setContentsMargins(10,10,10,0)
        layout.addWidget(description_label)
        
        
        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setFixedSize(QSize(300, 340))
        #self.setStyleSheet(r"QFrame { border-radius: 5px; background-color: white;}")


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
