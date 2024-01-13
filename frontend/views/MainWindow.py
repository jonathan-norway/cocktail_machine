import os
import sys
import logging
import platform

from PyQt5.QtWidgets import (QApplication,
                             QMainWindow, QStackedLayout, QVBoxLayout, QWidget)
app = QApplication(sys.argv)
from frontend import GuiConstants
from PyQt5.QtGui import QColor, QFontDatabase, QPalette
from frontend.views import CustomDrinkMenu, DrinkMenuView, ShotsMainMenu, UtilsMain
from frontend.views.MainMenu import MainView
from frontend.components.Headers import MainHeader

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
        self.setup_main_window()

    def setup_main_window(self):
        logger.info("Setting up main_window")
        self._add_font()
        self._configure_window()
        self.set_palette()

        self._set_central_widget()
        self._add_main_header()
        self._add_content_widget()

        self.add_views()
        logger.info("Finished setting up main_window")

    def _set_central_widget(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 0, 10, 5)
        main_layout_widget = QWidget()
        main_layout_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_layout_widget)

    def _add_font(self):
        current_directory = os.path.dirname(__file__)
        QFontDatabase.addApplicationFont(current_directory + "/roboto-regular.ttf")

    def _add_content_widget(self):
        self.content_layout = QStackedLayout()
        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)
        self.main_layout.addWidget(content_widget)

    def _add_main_header(self):
        self._main_header = MainHeader(navigate_to=self.navigate_to)
        dummy_layout = QVBoxLayout()
        dummy_layout.addWidget(self._main_header)
        dummy_widget = QWidget()
        dummy_widget.setLayout(dummy_layout)
        dummy_widget.setStyleSheet(
            "border-bottom: 2px solid black")
        self.main_layout.addWidget(dummy_widget)

    def _configure_window(self):
        self.setWindowTitle("MixMaster")
        self.resize(GuiConstants.MAX_WIDTH, GuiConstants.MAX_HEIGHT)
        if platform.system() != "Windows":
            self.showFullScreen()

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
        pallette.setColor(QPalette.ColorRole.Window, QColor(GuiConstants.color_palette["white"]))
        pallette.setColor(
            QPalette.ColorRole.WindowText, QColor(
                GuiConstants.color_palette["black"]))
        self.setPalette(pallette)

    def navigate_to(self, gui_view_enum: GuiConstants.GuiViews):
        logger.info(f"Navigating to {gui_view_enum.name}")
        if (gui_view_enum == GuiConstants.GuiViews.MAIN_MENU):
            self._main_header.main_menu_button.setVisible(False)
        else:
            self._main_header.main_menu_button.setVisible(True)
        self.content_layout.setCurrentIndex(gui_view_enum.value)
