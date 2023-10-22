import sys

from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton, QStackedLayout, QLabel, QVBoxLayout, QWidget,QHBoxLayout
from PyQt6.QtGui import QColor, QPalette, QFont, QFontDatabase, QPixmap
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
from GuiConstants import GuiViews
from views.MainMenu import MainView
from views.DrinkMenu import DrinkMenuView
color_palette = {
    "black": "#191919",
    "white": "#FFFFFF",
    "blue": "#05A3AD"
}



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        QFontDatabase.addApplicationFont("./roboto-regular.ttf")
        self.setWindowTitle("MixMaster")
        self.resize(1024, 600)
        
        self.set_palette()
        self.setup_main_window()
        
    def setup_main_window(self):
        main_layout = QVBoxLayout()
        
        main_layout.addWidget(self.get_header())
        self.content_layout = QStackedLayout()
        content_widget = QWidget()
        content_widget.setLayout(self.content_layout)
        content_widget.setFixedHeight(550)
        main_layout.addWidget(content_widget)
        main_layout_widget = QWidget()
        main_layout_widget.setLayout(main_layout)
        self.add_views()
        self.setCentralWidget(main_layout_widget)
        
    def add_views(self):
        content_layout = self.content_layout
        content_layout.addWidget(MainView(navigate_to=self.navigate_to))
        content_layout.addWidget(DrinkMenuView(navigate_func=self.navigate_to))
        self.content_layout.setCurrentIndex(1)
        
    def get_header(self) -> QLabel:
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        pixmap = QPixmap("icons/shaker.png")
        pixmap = pixmap.scaled(QSize(36,36), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmap_label = QLabel()
        pixmap_label.setPixmap(pixmap)
        header_layout.addWidget(pixmap_label)
        title_label = QLabel("MixMaster")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        title_font = QFont("Roboto", 32)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
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
        self.content_layout.setCurrentIndex(gui_view_enum.value)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()