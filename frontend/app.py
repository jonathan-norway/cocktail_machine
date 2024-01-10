import os
import sys
import logging
from typing import Callable
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QMainWindow, QPushButton, QSizePolicy,
                             QSpacerItem, QStackedLayout, QVBoxLayout, QWidget)
app = QApplication(sys.argv)
from frontend import GuiConstants
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
from frontend.views.Components.Headers import MainHeader


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        QFontDatabase.addApplicationFont(current_directory + "/roboto-regular.ttf")
        self.setWindowTitle("MixMaster")
        self.resize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        if platform.system() != "Windows":
            self.showFullScreen()
        self.set_palette()
        self.setup_main_window()

    def setup_main_window(self):
        logger.info("Setting up main_window")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 0, 10, 5)
        self._main_header = MainHeader(navigate_to=self.navigate_to)
        main_layout.addWidget(self._main_header)
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

    def set_palette(self):
        pallette = QPalette()
        pallette.setColor(QPalette.ColorRole.Window, QColor(color_palette["white"]))
        pallette.setColor(QPalette.ColorRole.WindowText, QColor(color_palette["black"]))
        self.setPalette(pallette)

    def navigate_to(self, gui_view_enum: GuiConstants.GuiViews):
        logger.info(f"Navigating to {gui_view_enum.name}")
        if (gui_view_enum == GuiConstants.GuiViews.MAIN_MENU):
            self._main_header.main_menu_button.setVisible(False)
        else:
            self._main_header.main_menu_button.setVisible(True)
        self.content_layout.setCurrentIndex(gui_view_enum.value)


def main():
    window = MainWindow()
    logger.info("Starting frontend through app.py")
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
