import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QScrollArea


class ScrollableListWidget(QScrollArea):
    def __init__(self):
        super(ScrollableListWidget, self).__init__()

        self.init_ui()

    def init_ui(self):
        # Create a scroll area

        # not-needed self.setWidgetResizable(False)

        # Create a widget to hold the list
        list_widget = QListWidget()
        list_widget.addItem("Item 1")
        list_widget.addItem("Item 2")
        list_widget.addItem("Item 3")
        list_widget.addItem("Item 4")
        list_widget.addItem("Item 5")

        # Set the widget as the content of the scroll area
        self.setWidget(list_widget)
