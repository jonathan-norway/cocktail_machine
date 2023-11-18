import os
from enum import Enum, auto
from typing import Callable

from GuiConstants import GuiViews, base_alcohols, color_palette
from PyQt6.QtCore import QSize, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QPixmap
from PyQt6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QProgressDialog
from .Labels import CenterQLabel


class PouringDrinkDialog(QWidget):
    def __init__(self):
        super(PouringDrinkDialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create a button to trigger the loading dialog
        button = QPushButton('Show Loading Dialog', self)
        button.clicked.connect(self.show_loading_dialog)
        layout.addWidget(button)

        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Loading Dialog Example')

    def show_loading_dialog(self):
        # Create a progress dialog with a determinate progress bar
        progress_dialog = QProgressDialog(self)
        progress_dialog.setLabelText('Loading...')
        progress_dialog.setRange(0, 100)  # Set the range from 0 to 100
        progress_dialog.setWindowTitle('Loading Dialog')
        progress_dialog.setWindowModality(2)  # Block interaction with the parent window

        # Create a timer to update the progress bar
        timer = QTimer(self)
        timer.timeout.connect(self.update_progress)
        timer.start(100)  # Update every 100 milliseconds (adjust as needed)

        # Show the dialog
        progress_dialog.exec()

        # Stop the timer when the dialog is closed
        timer.stop()

    def update_progress(self):
        # Increment the progress value
        progress_value = self.sender().value() + 1

        # Update the progress bar value
        self.sender().setValue(progress_value)
