
from typing import Callable

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from .Buttons import PreviousButton


class SecondHeader(QWidget):
    def __init__(self, title: str):
        super(SecondHeader, self).__init__()
        subheader_layout = QHBoxLayout()
        subheader_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.previous_button = PreviousButton()

        self.header_icon_label = QLabel()

        self.header_title = QLabel(title)
        font = self.header_title.font()
        font.setPointSize(26)
        self.header_title.setFont(font)
        subheader_spacing_item = QSpacerItem(
            150, 5
        )
        main_label_layout = QHBoxLayout()
        main_label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        main_label_layout.addWidget(self.header_icon_label)
        main_label_layout.addWidget(self.header_title)
        main_label_layout.setContentsMargins(0, 0, 0, 0)
        main_label_widget = QWidget()
        main_label_widget.setLayout(main_label_layout)
        subheader_layout.addSpacerItem(QSpacerItem(15, 5))
        subheader_layout.addWidget(
            self.previous_button, Qt.AlignmentFlag.AlignLeft
        )
        subheader_layout.addWidget(main_label_widget, Qt.AlignmentFlag.AlignCenter)
        subheader_layout.addItem(subheader_spacing_item)
        subheader_layout.setContentsMargins(0, 0, 0, 0)
        subheader_layout.setSpacing(0)
        self.setLayout(subheader_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.navigate_history = []
        self.navigate_func = None

    def update_header(self, title: str = None, icon_path: str = None,
                      navigate_func: Callable = None, navigate_history: list = None):
        if title:
            self.header_title.setText(title)
        if icon_path:
            subheader_pixmap = QPixmap(icon_path)
            subheader_pixmap = subheader_pixmap.scaled(
                QSize(36, 36),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.header_icon_label.setPixmap(subheader_pixmap)
            self.previous_button.update(navigate_func, navigate_history)
