
from typing import Callable

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from .Buttons import PreviousButton, MainMenuReturnButton
from frontend.icons import icon_dict


class MainHeader(QWidget):
    def __init__(self, navigate_to: Callable[[int], None]):
        super(MainHeader, self).__init__()
        self.setup_main_header(navigate_to)

    def setup_main_header(self, navigate_to):
        self.setLayout(QHBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        shaker_pixmap = QPixmap(icon_dict["shaker"])
        shaker_pixmap = shaker_pixmap.scaled(
            QSize(
                45,
                45),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        pixmap_label = QLabel()
        pixmap_label.setPixmap(shaker_pixmap)
        pixmap_label.setFixedSize(55, 55)
        title_label = QLabel("MixMaster")
        # self.setFixedHeight(85)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Roboto", 40)
        title_label.setFont(title_font)

        self.main_menu_button = MainMenuReturnButton(navigate_func=navigate_to)
        # self.main_menu_button.setStyleSheet("border-bottom: 2px solid blue;")
        self.main_menu_button.setVisible(False)
        HOME_BUTTON_SPACE_MODIFIER = 125
        self.layout().addSpacerItem(QSpacerItem(self.main_menu_button.width() + HOME_BUTTON_SPACE_MODIFIER, 5))
        self.layout().addWidget(pixmap_label)
        self.layout().addWidget(title_label)
        self.layout().addSpacerItem(QSpacerItem(pixmap_label.width() + HOME_BUTTON_SPACE_MODIFIER, 5))
        self.layout().addWidget(self.main_menu_button)
        self.setContentsMargins(0, 0, 0, 8)
        self.setFixedHeight(80)


class SecondHeader(QWidget):
    def __init__(self, title: str = "", ):
        super(SecondHeader, self).__init__()

        subheader_layout = QHBoxLayout()
        subheader_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._previous_button = PreviousButton()

        self.header_icon_label = QLabel()

        self.header_title = QLabel(title)
        font = self.header_title.font()
        font.setPointSize(26)
        self.header_title.setFont(font)
        main_label_layout = QHBoxLayout()
        main_label_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        main_label_layout.addWidget(self.header_icon_label)
        main_label_layout.addWidget(self.header_title)
        main_label_layout.setContentsMargins(0, 0, 0, 0)
        main_label_widget = QWidget()
        main_label_widget.setLayout(main_label_layout)
        button_spacer = QSpacerItem(35, 5)
        subheader_layout.addSpacerItem(button_spacer)
        subheader_layout.addWidget(
            self._previous_button, Qt.AlignmentFlag.AlignCenter
        )
        subheader_layout.addWidget(main_label_widget, Qt.AlignmentFlag.AlignCenter)
        subheader_layout.addItem(
            QSpacerItem(
                self._previous_button.size().width() +
                button_spacer.sizeHint().width(),
                5))
        subheader_layout.setContentsMargins(0, 0, 0, 0)
        subheader_layout.setSpacing(0)
        self.setLayout(subheader_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.navigate_func = None

    def update_header(self, title: str = None, icon_path: str = None,
                      navigate_func: Callable = None, navigate_history: list = None):
        if title:
            self.header_title.setText(title)

    def add_navigater(self, navigate_func: Callable[[None], None]) -> None:
        old_title = self.header_title.text()

        self._previous_button.update_nav(
            navigate_func, lambda: self.update_header(
                old_title))
