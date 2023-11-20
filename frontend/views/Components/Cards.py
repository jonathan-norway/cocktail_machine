from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)
from typing import Callable


class Card(QFrame):
    def __init__(
        self, icon_path: str, title: str, description: str, on_click: Callable
    ):
        super(Card, self).__init__()
        self.on_click = on_click
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

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        description_font = description_label.font()
        description_font.setPointSize(14)
        description_label.setFont(description_font)
        description_label.setFixedWidth(250)
        self.main_layout.addWidget(description_label)
        # description_label.setStyleSheet("QLabel {border: 2px solid red}")
        self.setFixedSize(QSize(290, 160))
        # self.setStyleSheet("border: 2px solid red;")
        self.setFrameStyle(1)
        self.setLineWidth(1)
        # self.setContentsMargins(5,10,5,0)

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
        # self.setContentsMargins(0,0,0,0)
        # self.setFixedSize(QSize(600,450))
        # self.setStyleSheet("border: 2px solid red")

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
