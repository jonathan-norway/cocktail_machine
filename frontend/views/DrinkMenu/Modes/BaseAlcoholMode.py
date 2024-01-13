from frontend.components import CardList, Card, DrinkCard
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from frontend.GuiConstants import base_alcohols
from typing import Callable

import logging
logger = logging.getLogger(__name__)


class BaseAlcoholMode(CardList):
    def __init__(self, select_base_alcohol: Callable[[str], None]):
        super(BaseAlcoholMode, self).__init__()
        self.setup_base_alcohol_mode(select_base_alcohol)

    def setup_base_alcohol_mode(self, select_base_alcohol: Callable[[str], None]):
        logger.info("Setting up BaseAlcoholmode")
        for base_alcohol in base_alcohols:
            self.add_card(
                Card(
                    title=base_alcohol["name"],
                    description=base_alcohol["description"],
                    icon_path=base_alcohol["icon"],
                    on_click=lambda name=base_alcohol["name"]: select_base_alcohol(name)
                )
            )
            logger.debug(f"Added card for {base_alcohol!r}")
        logger.info("Finished setting up BaseAlcoholmode")
