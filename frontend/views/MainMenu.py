from typing import Callable
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
import logging

from .Components import NavCard
from frontend.GuiConstants import GuiViews
from frontend.icons import icon_dict

logger = logging.getLogger(__name__)


class MainView(QWidget):
    MAX_CARDS_PER_LINE = 2

    def __init__(self, navigate_to: Callable):
        logger.info("Initializing MainView")
        super(MainView, self).__init__()
        self.setup_view(navigate_to)
        logger.info("Finished initializing MainView")

    def setup_view(self, navigate_to: Callable[[int], None]) -> None:
        self.setLayout(QVBoxLayout())
        self.layout_list = []

        nav_cards = [
            NavCard(
                "Drink Menu",
                lambda: navigate_to(
                    GuiViews.DRINK_MENU),
                icon_dict["cocktail"]
            ),
            NavCard(
                "Custom Drink",
                lambda: navigate_to(
                    GuiViews.CUSTOM_DRINK),
                icon_dict["bottles"]
            ),
            NavCard(
                "Shots",
                lambda: navigate_to(
                    GuiViews.SHOTS),
                icon_dict["shot"]
            ),
            NavCard(
                "Utils",
                lambda: navigate_to(
                    GuiViews.UTILS),
                icon_dict["tools"]
            )
        ]
        for nav_card in nav_cards:
            current_layout = self.get_current_layout_or_create_new()
            current_layout.addWidget(nav_card)

    @staticmethod
    def _create_new_h_layout_widget():
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setSpacing(10)
        return horizontal_layout

    def get_current_layout_or_create_new(self):
        if len(
                self.layout_list) == 0 or self.layout_list[-1].count() >= MainView.MAX_CARDS_PER_LINE:
            h_layout = MainView._create_new_h_layout_widget()
            self.layout().addLayout(h_layout)
            self.layout_list.append(h_layout)
            return h_layout
        else:
            return self.layout_list[-1].layout()
