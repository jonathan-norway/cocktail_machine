from enum import Enum, auto
from typing import Callable

from frontend.GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from typing import List


class ModeMenuLayout(QVBoxLayout):
    def __init__(self, max_per_row=3):
        super(ModeMenuLayout, self).__init__()
        self._MAX_PER_ROW = max_per_row
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSpacing(20)
        self.horizontal_layouts: List[QHBoxLayout] = []
        # self.addLayout(self.get_QHBoxLayout())

    def addWidget(self, widget_to_add: QWidget):
        was_added = False
        for layout in self.horizontal_layouts:
            if layout.count() >= self._MAX_PER_ROW:
                continue
            was_added = True
            layout.addWidget(widget_to_add)
        if not was_added:
            temp_layout = self.get_QHBoxLayout()
            temp_layout.addWidget(widget_to_add)

    def get_QHBoxLayout(self):
        temp_QHBox_Layout = QHBoxLayout()
        self.horizontal_layouts.append(temp_QHBox_Layout)
        self.addLayout(temp_QHBox_Layout)
        return temp_QHBox_Layout


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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.on_click = on_click

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_font = title_label.font()
        title_font.setPointSize(22)
        title_label.setFont(title_font)
        title_label.setContentsMargins(0, 15, 0, 20)
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
        description_label.setContentsMargins(10, 10, 10, 0)
        layout.addWidget(description_label)

        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setFixedSize(QSize(290, 340))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()
