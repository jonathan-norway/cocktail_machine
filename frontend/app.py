import os
import sys
import logging
from typing import Callable
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSizePolicy,
                             QSpacerItem, QStackedLayout, QVBoxLayout, QWidget)
app = QApplication(sys.argv)
import GuiConstants
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QFont, QFontDatabase, QIcon, QPalette, QPixmap
from frontend.views import CustomDrinkMenu, DrinkMenuView, ShotsMainMenu, UtilsMain
from frontend.views.MainMenu import MainView
color_palette = {
    "black": "#191919",
    "white": "#FFFFFF",
    "blue": "#05A3AD"
}
current_directory = os.path.dirname(__file__)
import platform
logger = logging.getLogger("frontend")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(
    'logs/frontend.log',
    mode='w',
    encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setStyleSheet("border: 1px solid red")
        QFontDatabase.addApplicationFont(current_directory + "/roboto-regular.ttf")
        self.setWindowTitle("MixMaster")
        self.resize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        if platform.system() != "Windows":
            self.showFullScreen()
        # self.setFixedSize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        self.set_palette()
        self.setup_main_window()

    def setup_main_window(self):
        logger.info("Setting up main_window")
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
        logger.info("Finished setting up main_window")

    def add_views(self):
        logger.info("Adding views to main_window")
        content_layout = self.content_layout
        content_layout.addWidget(MainView(navigate_to=self.navigate_to))
        content_layout.addWidget(DrinkMenuView())
        content_layout.addWidget(CustomDrinkMenu())
        content_layout.addWidget(ShotsMainMenu())
        content_layout.addWidget(UtilsMain())
        logger.info("Finished adding views to main_window")
        # self.content_layout.setCurrentIndex(1)

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

    def navigate_to(self, gui_view_enum: GuiConstants.GuiViews):
        logger.info(f"Navigating to {gui_view_enum.name}")
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


def main():
    window = MainWindow()
    logger.info("Starting frontend through app.py")
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
