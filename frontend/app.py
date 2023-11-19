import os
import sys
from pathlib import Path
from typing import Callable

import GuiConstants
from PIL import Image
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSizePolicy,
                             QSpacerItem, QStackedLayout, QVBoxLayout, QWidget)
from views import CustomDrinkMenu, DrinkMenuView, ShotsMainMenu, UtilsMain
from views.MainMenu import MainView

color_palette = {
    "black": "#191919",
    "white": "#FFFFFF",
    "blue": "#05A3AD"
}
current_directory = os.path.dirname(__file__)
import platform


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setStyleSheet("border: 1px solid red")
        QFontDatabase.addApplicationFont(current_directory + "/roboto-regular.ttf")
        self.setWindowTitle("MixMaster")
        self.resize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        if platform.system() != "Windows":
            self.showFullScreen()
            # print("SHOULD BE FULLSCREEN SOON")
        # self.setFixedSize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        self.set_palette()

        self.setup_main_window()

    def setup_main_window(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 0, 10, 5)
        main_layout.addWidget(self.get_header())
        self.content_layout = QStackedLayout()
        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)
        content_widget.setFixedHeight(450)
        main_layout.addWidget(content_widget)
        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)
        self.add_views()
        self.setCentralWidget(main_layout_widget)

    def add_views(self):
        content_layout = self.content_layout
        content_layout.addWidget(MainView(navigate_to=self.navigate_to))
        content_layout.addWidget(DrinkMenuView())
        content_layout.addWidget(CustomDrinkMenu())
        content_layout.addWidget(ShotsMainMenu())
        content_layout.addWidget(UtilsMain())
        self.content_layout.setCurrentIndex(1)

    def get_header(self) -> QWidget:
        header_layout = QHBoxLayout()

        header_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        shaker_pixmap = QPixmap(current_directory + "/icons/shaker.png")
        shaker_pixmap = shaker_pixmap.scaled(
            QSize(
                45,
                45),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        pixmap_label = QLabel()
        pixmap_label.setPixmap(shaker_pixmap)
        pixmap_label.setFixedSize(55, 55)
        header_layout.addWidget(pixmap_label)
        title_label = QLabel("MixMaster")
        title_label.setFixedWidth(250)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Roboto", 40)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        subheader_spacing_item = QSpacerItem(
            225, 5
        )
        header_layout.addSpacerItem(subheader_spacing_item)
        self.main_menu_button = MainMenuReturnButton(navigate_func=self.navigate_to)
        header_layout.addWidget(self.main_menu_button)
        header_layout.addSpacerItem(QSpacerItem(30, 5))
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("border-bottom: 2px solid black")
        return header_widget

    def set_palette(self):
        pallette = QPalette()
        pallette.setColor(QPalette.ColorRole.Window, QColor(color_palette["white"]))
        pallette.setColor(QPalette.ColorRole.WindowText, QColor(color_palette["black"]))
        self.setPalette(pallette)

    def button_clicked(self, s):
        print("click", s)

        dlg = QDialog(self)
        dlg.setWindowTitle("HELLO!")
        dlg.exec()

    def navigate_to(self, gui_view_enum):
        if (gui_view_enum == GuiConstants.GuiViews.MAIN_MENU):
            self.main_menu_button.setVisible(False)
        else:
            self.main_menu_button.setVisible(True)
        self.content_layout.setCurrentIndex(gui_view_enum.value)


class MainMenuReturnButton(QWidget):
    def __init__(self, navigate_func: Callable):
        super(MainMenuReturnButton, self).__init__()
        return_pixmap = QPixmap(current_directory + "/icons/house.png")
        return_pixmap = return_pixmap.scaled(
            QSize(
                55,
                55),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        sizePolicy = self.sizePolicy()
        sizePolicy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(sizePolicy)
        self.return_label = QLabel()
        self.return_label.setPixmap(return_pixmap)
        self.return_label.setFixedSize(60, 60)
        self.navigate_func = navigate_func
        default_layout = QHBoxLayout()
        default_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        default_layout.addWidget(self.return_label)
        self.setLayout(default_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.navigate_func(GuiConstants.GuiViews.MAIN_MENU)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
