import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator


class SliderWithLabel(QWidget):

    internalValueUpdate = pyqtSignal(int)

    def __init__(self, title: str, constant: float, lower: int = 0, upper: int = 10_000):
        super(SliderWithLabel, self).__init__()
        self.CONSTANT = constant
        self.title_label = QLabel(text=title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(lower, upper)
        # ? self.slider.setValue(0)
        self.slider.valueChanged.connect(self.valueUpdate)

        self.int_validator = QIntValidator()
        self.line_edit = QLineEdit()
        self.line_edit.setValidator(self.int_validator)
        self.line_edit.textChanged.connect(self.valueUpdate)

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.line_edit)
        # Update the label initially

    def valueUpdate(self, value):
        self.update_internal_value(value)
        self.internalValueUpdate.emit(value)

    def update_internal_value(self, value: int):
        print(f"{value=}")
        try:
            sanitized_value = int(value)
        except Exception as e:
            sanitized_value = 0
        try:
            sanitized_line_edit_value = int(self.line_edit.text())
        except Exception as e:
            sanitized_line_edit_value = 0

        if self.slider.value() != sanitized_value:
            self.slider.setValue(sanitized_value)
        if sanitized_line_edit_value != sanitized_value and sanitized_line_edit_value != 0:
            self.line_edit.setText(str(sanitized_value))

    def update_external_value(self, new_value: int):
        try:
            sanitized_value = int(self.line_edit.text())
        except BaseException:
            sanitized_value = 0
        if sanitized_value == new_value * self.CONSTANT:
            return
        self.update_internal_value(new_value * self.CONSTANT)


ML_P_MS = 0.045


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Number Slider Example")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.init_ui()

    def init_ui(self):
        # Create a slider
        self.millisecond_slider = SliderWithLabel("Milliseconds", 1 / ML_P_MS, 0, 8_000)
        self.millilitre_slider = SliderWithLabel("Millilitre", ML_P_MS, 0, 300)
        self.millisecond_slider.internalValueUpdate.connect(
            self.millilitre_slider.update_external_value)
        self.millilitre_slider.internalValueUpdate.connect(
            self.millisecond_slider.update_external_value)
        # Set up the layout
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.millisecond_slider)

        horizontal_layout = QHBoxLayout()

        constant_label = QLabel("ML_P_MS FACTOR: ")
        self.constant_field = QLineEdit()
        self.constant_field.setValidator(QIntValidator())
        self.constant_field.setText(str(ML_P_MS))

        horizontal_layout.addWidget(constant_label)
        horizontal_layout.addWidget(self.constant_field)

        layout.addLayout(horizontal_layout)
        layout.addWidget(self.millilitre_slider)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
