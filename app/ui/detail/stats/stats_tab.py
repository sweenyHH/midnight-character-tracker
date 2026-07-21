from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from app.ui.detail.utils import get_layout
from app.ui.detail.stats.attributes_widget import AttributesWidget
from app.ui.detail.stats.combat_ratings_widget import CombatRatingsWidget
from app.ui.detail.stats.equipment_widget import EquipmentWidget


class StatsTab(QWidget):

    def __init__(self):
        super().__init__()

        self.attributes_widget = (AttributesWidget())
        self.combat_ratings_widget = (CombatRatingsWidget())
        self.equipment_widget = (EquipmentWidget())

        self.container = QWidget()
        self.main_layout = QHBoxLayout(self.container)

# LEFT SIDE

        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.left_layout.addWidget(self.attributes_widget)
        self.left_layout.addWidget(self.combat_ratings_widget)
        self.left_layout.setAlignment(Qt.AlignTop)

# MAIN LAYOUT

        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.equipment_widget)
        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 3)

        layout = get_layout(self)
        layout.addWidget(self.container)


    def set_character(self, character):
      
        self.attributes_widget.set_character(character)
        self.combat_ratings_widget.set_character(character)
        self.equipment_widget.set_character(character)