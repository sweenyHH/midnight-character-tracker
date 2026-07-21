from PySide6.QtWidgets import (
QWidget,
QVBoxLayout,
QHBoxLayout,
)

from app.ui.detail.overview.pvp_card import PvpCard
from app.ui.detail.overview.resource_card import ResourceCard
from app.ui.detail.overview.character_card import CharacterCard
from app.ui.detail.overview.pve_card import PveCard


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(12)


        self.character_card = CharacterCard()
        self.resources_card = ResourceCard()
        self.pvp_card = PvpCard()
        self.pve_card = PveCard()



        self.top_row = QHBoxLayout()
        self.bottom_row = QHBoxLayout()


        self.top_row.addWidget(
            self.character_card,
            1
        )

        self.top_row.addWidget(
            self.pve_card,
            1
        )

        self.bottom_row.addWidget(
            self.resources_card,
            1
        )

        self.bottom_row.addWidget(
            self.pvp_card,
            1
        )

        self.main_layout.addLayout(
            self.top_row
        )

        self.main_layout.addLayout(
            self.bottom_row
        )


        self.main_layout.addStretch()

    def set_character(self, character):

        self.character_card.set_character(character)
        self.pvp_card.set_character(character)
        self.resources_card.set_character(character)
        self.pve_card.set_character(character)

 
