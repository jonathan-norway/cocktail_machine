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
 
 
class ModeMenuLayout(QHBoxLayout):
    def __init__(self):
        super(ModeMenuLayout, self).__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSpacing(20)
    


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
        self.setFixedSize(QSize(290, 340))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()

