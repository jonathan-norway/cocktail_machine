from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class CenterQLabel(QLabel):
    def __init__(self, title: str = None):
        super(CenterQLabel, self).__init__(text=title)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setContentsMargins(0, 0, 0, 0)