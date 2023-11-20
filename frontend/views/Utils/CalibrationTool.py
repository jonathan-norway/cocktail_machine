import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator


class SliderWithLabel(QWidget):

    internalValueUpdate = pyqtSignal(int)

    def __init__(self, title: str, constant: float, lower: int, upper: int):
        super(SliderWithLabel, self).__init__()
        self.CONSTANT = constant

        self.title_label = QLabel(text=title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(lower, upper)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.valueUpdate)

        self.line_edit = QLineEdit()
        self.line_edit.setText("0")
        self.line_edit.setValidator(QIntValidator())
        self.line_edit.textChanged.connect(self.update_internal_value)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.line_edit)

    def valueUpdate(self, value):
        self.update_internal_value(value)
        self.internalValueUpdate.emit(value)

    def update_internal_value(self, value: float):
        print(f"{value=}")
        try:
            sanitized_value = float(value)
        except Exception as e:
            sanitized_value = 0
        try:
            sanitized_line_edit_value = float(self.line_edit.text())
        except Exception as e:
            sanitized_line_edit_value = 0

        if self.slider.value() != sanitized_value:
            self.slider.setValue(int(sanitized_value))
        if sanitized_line_edit_value != sanitized_value:
            self.line_edit.setText(str(sanitized_value))

    def update_external_value(self, new_value: float):
        try:
            sanitized_value = float(self.line_edit.text())
        except BaseException:
            sanitized_value = 0
        if sanitized_value == new_value * self.CONSTANT:
            return
        self.update_internal_value(new_value * self.CONSTANT)


class CalibrationToolLayout(QVBoxLayout):
    ML_P_MS = 0.0045

    def __init__(self):
        super(CalibrationToolLayout, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Create a slider
        self.millisecond_slider = SliderWithLabel("Milliseconds", 1 / self.ML_P_MS, 0, 16_000)
        self.millilitre_slider = SliderWithLabel("Millilitre", self.ML_P_MS, 0, 300)
        self.millisecond_slider.internalValueUpdate.connect(
            self.millilitre_slider.update_external_value)
        self.millilitre_slider.internalValueUpdate.connect(
            self.millisecond_slider.update_external_value)

        constant_label = QLabel("ML_P_MS RATIO: ")
        self.constant_field = QLineEdit()
        self.constant_field.setValidator(QIntValidator())
        self.constant_field.setText(str(self.ML_P_MS))

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(constant_label)
        horizontal_layout.addWidget(self.constant_field)

        self.addWidget(self.millisecond_slider)
        self.addLayout(horizontal_layout)
        self.addWidget(self.millilitre_slider)


class CalibrationTool(QWidget):
    def __init__(self):
        super(CalibrationTool, self).__init__()
        self.setLayout(CalibrationToolLayout())
        self.setFixedWidth(500)
