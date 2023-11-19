import math
import os
from pathlib import Path
from typing import Callable

import qrcode
from PyQt5.QtCore import QObjectCleanupHandler, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QGridLayout,
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
                             QPushButton, QSizePolicy, QSpacerItem,
                             QStackedLayout, QVBoxLayout, QWidget)

from backend.cocktail_machine import CocktailMachine
from backend.datatypes import CocktailRecipe

from .Labels import CenterQLabel
from .Buttons import MakeMeADrinkButton

current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
import io


def generate_qr_code(data, size=200):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    img_bytes = io.BytesIO()
    qr_img.save(img_bytes, format="PNG")
    img_data = img_bytes.getvalue()

    qimage = QImage.fromData(img_data)
    pixmap = QPixmap.fromImage(qimage)

    return pixmap


class DrinkCard(QFrame):
    def __init__(
        self, title: str, icon_path: str, description: str, on_click: Callable
    ):
        super(DrinkCard, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)
        self.add_title(title)
        self.add_icon(icon_path)
        self.add_description(description)
        # self.add_indicators() for ex. sweetness/ratings/how many made?

        self.on_click = on_click

        self.setFrameStyle(1)
        self.setLineWidth(1)
        self.setFixedSize(QSize(290, 340))

    def add_title(self, title):
        self.title_label = CenterQLabel(title)
        self.main_layout.addWidget(self.title_label)
        self.title_label.setFixedHeight(65)
        self.title_label.setContentsMargins(10, 15, 10, 15)
        font = self.title_label.font()
        font.setCapitalization(QFont.Capitalization.Capitalize)
        font.setPointSize(18)
        self.title_label.setFont(font)

    def add_icon(self, icon_path: str):
        icon_label = CenterQLabel()
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(50, 50)
        icon_label.setPixmap(pixmap)
        self.main_layout.addWidget(icon_label)

    def add_description(self, description: str):
        description_label = CenterQLabel(
            description if len(description) < 60 else description[:60]
        )
        description_label.setWordWrap(True)
        description_label.setContentsMargins(15, 0, 15, 0)
        font = description_label.font()
        font.setPointSize(14)
        description_label.setFont(font)
        self.main_layout.addWidget(description_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print(f"CLICKED ON {self.title_label.text()}")
            self.on_click()


ITEMS_TO_SHOW = 4


class DrinkList(QWidget):
    def __init__(self, items=[], items_per_line=4, total_lines=1):
        super(DrinkList, self).__init__()
        self.page = 0
        self.items_per_line = items_per_line
        self.total_lines = total_lines
        self.main_setup()
        self.set_items(items)

    def set_items(self, items: list):
        self.items = items
        while self.stacked_layout.count():
            item = self.stacked_layout.takeAt(0)
            if item:
                item.widget().deleteLater()
        self.setup_stacked_layout()

    def main_setup(self):
        main_layout = QVBoxLayout()
        self.stacked_layout = QStackedLayout()

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.previous_button = ListNavigateButton(
            icon_path=current_directory + "/icons/return.png",
            on_click=self.load_previous,
        )
        # self.previous_button.clicked.connect(self.load_previous)
        self.next_button = ListNavigateButton(
            icon_path=current_directory + "/icons/next-page.png",
            on_click=self.load_next,
        )
        # self.next_button.clicked.connect()
        button_layout.addWidget(self.previous_button)
        button_layout.addSpacerItem(QSpacerItem(30, 5))
        button_layout.addWidget(self.next_button)

        self.stacked_layout_widget = QWidget()
        self.stacked_layout_widget.setLayout(self.stacked_layout)
        main_layout.addWidget(self.stacked_layout_widget)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def setup_stacked_layout(self):
        stacked_layout = self.stacked_layout
        self.horizontal_layouts = [
            QHBoxLayout() for _ in range(math.ceil(len(self.items) / ITEMS_TO_SHOW))
        ]
        for index, item in enumerate(self.items):
            item.setFixedWidth(230)
            self.horizontal_layouts[index // ITEMS_TO_SHOW].addWidget(item)
        for layout in self.horizontal_layouts:
            widget = QWidget()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget.setLayout(layout)
            stacked_layout.addWidget(widget)
        # self.setLayout(main_layout)

    def load_next(self):
        print("trying to load next")
        if self.can_go_next():
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() + 1)

            if not self.can_go_next():
                self.next_button.setHidden(True)
            self.previous_button.setHidden(False)

    def load_previous(self):
        print("trying to load previous")
        if self.can_go_back():
            print("went back")
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() - 1)
            if not self.can_go_back():
                self.previous_button.setHidden(True)
            self.next_button.setHidden(False)

    def can_go_back(self) -> bool:
        return 0 < self.stacked_layout.currentIndex()

    def can_go_next(self) -> bool:
        return self.stacked_layout.count() - 1 > self.stacked_layout.currentIndex()


class ListNavigateButton(QWidget):
    def __init__(self, icon_path: str, on_click: Callable):
        super(ListNavigateButton, self).__init__()
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(50, 36)
        button_label = QLabel()
        button_label.setPixmap(pixmap)
        size_policy = self.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
        layout = QHBoxLayout()
        layout.addWidget(button_label)
        self.on_click = on_click
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.on_click()


class DetailedDrinkView(QWidget):
    def __init__(self):
        super(DetailedDrinkView, self).__init__()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

    def set_new_drink(self, cocktail: CocktailRecipe):
        self.cocktail = cocktail

        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.setup()

    def setup(self):
        self.add_side_pane()
        self.add_grid_spacer()
        self.add_main_content()
        self.add_bottom_spacer()

    def add_side_pane(self):
        self.add_icon()
        self.add_tags()
        self.add_origin()
        # self.add_stats()
        self.add_QR_code()

    def add_grid_spacer(self):
        widget = QSpacerItem(
            40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.main_layout.addItem(widget, 0, 4, 10, 2)

    def add_main_content(self):
        self.add_title()
        self.add_description()
        self.add_steps()
        self.add_submit_button()

    def add_icon(self):
        default_path = current_directory + "/icons/cocktail.png"
        potential_path = (
            current_directory + f"/icons/drinks/{self.cocktail.name.lower()}.png"
        )
        icon_pixmap = QPixmap(
            potential_path if Path(potential_path).exists() else default_path
        )
        icon_pixmap = icon_pixmap.scaled(QSize(110, 110))
        icon_label = CenterQLabel()
        icon_label.setPixmap(icon_pixmap)
        self.main_layout.addWidget(icon_label, 0, 1, 3, 3)

    def add_tags(self):
        tags = self.cocktail.tags
        TAGS_PER_LINE = 2
        vertical_layout = QVBoxLayout()
        vertical_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # vertical_layout.setSpacing(0)
        vertical_layout.setContentsMargins(0, 10, 0, 0)
        horizontal_layouts = [
            QHBoxLayout() for _ in range(math.ceil(len(tags) / TAGS_PER_LINE))
        ]
        for index, tag in enumerate(tags):
            drink_tag = DrinkTag(tag)
            horizontal_layouts[index // TAGS_PER_LINE].addWidget(drink_tag)

        for h_layout in horizontal_layouts:
            h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            vertical_layout.addLayout(h_layout)

        self.main_layout.addLayout(vertical_layout, 4, 1, 2, 3)

    def add_origin(self):
        origin_country = self.cocktail.origin_country
        if not origin_country or not Path(
            current_directory + f"icons/flags/{origin_country}"
        ):
            return
        flag_pixmap = QPixmap(current_directory + f"/icons/flags/{origin_country}")
        flag_pixmap = flag_pixmap.scaled(150, 150)
        flag_label = CenterQLabel()
        flag_label.setContentsMargins(0, 15, 0, 0)
        flag_label.setPixmap(flag_pixmap)
        self.main_layout.addWidget(flag_label, 5, 1, 3, 3)

    def add_QR_code(self):
        qr_pixmap = generate_qr_code(self.cocktail.external_link, 50)
        qr_pixmap = qr_pixmap.scaled(140, 140)
        pixmap_label = CenterQLabel()
        pixmap_label.setPixmap(qr_pixmap)
        self.main_layout.addWidget(pixmap_label, 9, 1, 4, 3)

    def add_title(self):
        cocktail_name = self.cocktail.name
        title_label = QLabel(text=cocktail_name)
        font = title_label.font()
        font.setPointSize(22)
        font.setCapitalization(QFont.Capitalization.Capitalize)
        font.setUnderline(True)
        title_label.setFont(font)
        self.main_layout.addWidget(title_label, 0, 6, 1, 5)

    def add_description(self):
        cocktail_description = self.cocktail.description
        description_label = QLabel(text=cocktail_description)
        description_label.setWordWrap(True)
        font = description_label.font()
        font.setPointSize(14)
        description_label.setFont(font)
        self.main_layout.addWidget(description_label, 1, 6, 5, 4)

    def add_steps(self):
        steps = self.cocktail.steps
        text = ""
        for index, step in enumerate(steps):
            text += f"{index + 1}. " + step + "<br>"
        steps_label = QLabel(text)
        steps_label.setContentsMargins(10, 0, 0, 0)
        font = steps_label.font()
        font.setPointSize(14)
        steps_label.setFont(font)
        self.main_layout.addWidget(steps_label, 6, 6, 6, 4)

    def add_submit_button(self):
        submit_button = MakeMeADrinkButton(
            on_click=lambda: CocktailMachine.pour_cocktail(
                self.cocktail.name))
        submit_button.setContentsMargins(20, 0, 0, 0)
        self.main_layout.addWidget(submit_button, 11, 6, 2, 4)

    def add_bottom_spacer(self):
        widget = QSpacerItem(
            100, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.main_layout.addItem(widget, 13, 0, 1, 10)


class DrinkTag(QLabel):
    def __init__(self, tag_message: str):
        super(DrinkTag, self).__init__(tag_message)
        self.setFixedSize(QSize(70, 25))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
        self.setStyleSheet("QLabel {border-radius: 15px; background-color: #ffefef}")
