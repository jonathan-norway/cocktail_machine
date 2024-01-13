from frontend.components import CardList, Card
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QGridLayout, QSpacerItem, QSizePolicy
from frontend.GuiConstants import base_alcohols
from backend import CocktailRecipe
from frontend.icons import icon_dict
import math
import io
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

from frontend.components.Labels import CenterQLabel
from frontend.components.Buttons import MakeMeADrinkButton


class DetailedDrinkDisplayMode(QWidget):
    def __init__(self):
        super(DetailedDrinkDisplayMode, self).__init__()
        self.setLayout(QGridLayout())

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
        self.layout().addItem(widget, 0, 4, 10, 2)

    def add_main_content(self):
        self.add_title()
        self.add_description()
        self.add_steps()
        self.add_submit_button()

    def add_icon(self):
        default_path = icon_dict["cocktail"]
        potential_path = icon_dict.get("_".join(self.cocktail.name.lower().split()))
        icon_pixmap = QPixmap(
            potential_path if potential_path else default_path
        )
        icon_pixmap = icon_pixmap.scaled(QSize(110, 110))
        icon_label = CenterQLabel()
        icon_label.setPixmap(icon_pixmap)
        self.layout().addWidget(icon_label, 0, 1, 3, 3)

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

        self.layout().addLayout(vertical_layout, 4, 1, 2, 3)

    def add_origin(self):
        origin_country = self.cocktail.origin_country
        print(f"{origin_country=}")
        if not origin_country or not icon_dict.get(origin_country.lower()):
            return
        flag_pixmap = QPixmap(icon_dict[origin_country.lower()])
        flag_pixmap = flag_pixmap.scaled(150, 150)
        flag_label = CenterQLabel()
        flag_label.setContentsMargins(0, 15, 0, 0)
        flag_label.setPixmap(flag_pixmap)
        self.layout().addWidget(flag_label, 5, 1, 3, 3)

    def add_QR_code(self):
        qr_pixmap = generate_qr_code(self.cocktail.external_link, 50)
        qr_pixmap = qr_pixmap.scaled(140, 140)
        pixmap_label = CenterQLabel()
        pixmap_label.setPixmap(qr_pixmap)
        self.layout().addWidget(pixmap_label, 9, 1, 4, 3)

    def add_title(self):
        # cocktail_name = self.cocktail.name
        # title_label = QLabel(text=cocktail_name)
        # font = title_label.font()
        # font.setPointSize(22)
        # font.setCapitalization(QFont.Capitalization.Capitalize)
        # font.setUnderline(True)
        # title_label.setFont(font)
        # self.layout().addWidget(title_label, 0, 6, 1, 5)
        pass

    def add_description(self):
        cocktail_description = self.cocktail.description
        description_label = QLabel(text=cocktail_description)
        description_label.setWordWrap(True)
        font = description_label.font()
        font.setPointSize(14)
        description_label.setFont(font)
        self.layout().addWidget(description_label, 1, 6, 5, 4)

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
        self.layout().addWidget(steps_label, 6, 6, 6, 4)

    def add_submit_button(self):
        submit_button = MakeMeADrinkButton(
            on_click=lambda: CocktailMachine.pour_cocktail(
                self.cocktail.name))
        submit_button.setContentsMargins(20, 0, 0, 0)
        self.layout().addWidget(submit_button, 11, 6, 2, 4)

    def add_bottom_spacer(self):
        widget = QSpacerItem(
            100, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.layout().addItem(widget, 13, 0, 1, 10)

    def set_new_drink(self, cocktail: CocktailRecipe):
        self.cocktail = cocktail

        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.setup()


class DrinkTag(QLabel):
    def __init__(self, tag_message: str):
        super(DrinkTag, self).__init__(tag_message)
        self.setFixedSize(QSize(70, 25))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
        self.setStyleSheet("QLabel {border-radius: 15px; background-color: #ffefef}")


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
