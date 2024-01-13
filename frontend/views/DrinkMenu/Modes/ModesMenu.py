import logging
from typing import Callable
from frontend.components import ModeMenuLayout, MenuModeCard
from PyQt5.QtWidgets import QWidget
from frontend.icons import icon_dict
from frontend.GuiConstants import DrinkMenuModes

logger = logging.getLogger(__name__)


class ModesMenu(QWidget):
    def __init__(self, navigate_to: Callable[[int, str], None]):
        super(ModesMenu, self).__init__()
        logger.info(f"Initializing {__name__}")
        self._setup_modes_menu(navigate_to)
        logger.info(f"Finished initializing {__name__}")

    def _setup_modes_menu(self, navigate_to: Callable[[int, str], None]):
        modes = [
            MenuModeCard(
                title="Popularity",
                icon_path=icon_dict["popularity"],
                description="Select a drink based on popularity. You cannot go wrong with a fan favorite!",
                on_click=lambda: navigate_to(DrinkMenuModes.POPULARITY, "Popularity"),
            ),
            MenuModeCard(
                title="Base Alcohol",
                icon_path=icon_dict["bottles"],
                description="Select a drink based on a specific base alcohol, or try a new one!",
                on_click=lambda: navigate_to(DrinkMenuModes.BASE_ALCOHOL, "Base Alcohol"),
            ),
            MenuModeCard(
                title="Mood",
                icon_path=icon_dict["season"],
                description="Select a drink based on your mood, season, or planet orientation.",
                on_click=lambda: navigate_to(DrinkMenuModes.MOOD, "Mood"),
            )
        ]
        self.setLayout(ModeMenuLayout())
        for mode in modes:
            self.layout().addWidget(mode)
            logger.debug(f"Added MenuModeCard {mode!r}")
