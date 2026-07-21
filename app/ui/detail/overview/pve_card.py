from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
)

from app.ui.blizzard_color_codes import get_mplus_color

from app.storage.vault_storage import load_user_vault

from app.localization.ui_strings import get_ui_string


class PveCard(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("overviewCard")
        self.setFrameShape(QFrame.Box)

        layout = QVBoxLayout(self)

        self.pve_title = QLabel()
        self.pve_title.setObjectName("overviewSectionTitle")

        layout.addWidget(self.pve_title)

        tiles_row = QHBoxLayout()

        layout.addLayout(tiles_row)

        # Mythic+

        self.mplus_tile = QFrame()
        self.mplus_tile.setObjectName("overviewTile")
        self.mplus_tile.setFrameShape(QFrame.Box)

        mplus_layout = QVBoxLayout(self.mplus_tile)

        self.mplus_tile_title = QLabel()
        self.mythic_score_label = QLabel()
        self.mythic_score_label.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            """
        )

        mplus_layout.addWidget(self.mplus_tile_title)
        mplus_layout.addWidget(self.mythic_score_label)

        tiles_row.addWidget(self.mplus_tile, 1)

        # Vault

        self.vault_tile = QFrame()
        self.vault_tile.setObjectName("overviewTile")
        self.vault_tile.setFrameShape(QFrame.Box)

        vault_layout = QVBoxLayout(self.vault_tile)

        self.vault_tile_title = QLabel()

        vault_layout.addWidget(self.vault_tile_title)
        vault_grid = QGridLayout()
        vault_layout.addLayout(vault_grid)

        self.vault_delves_name = QLabel()
        self.vault_raid_name = QLabel()
        self.vault_mplus_name = QLabel()

        self.vault_delves_value = QLabel()
        self.vault_raid_value = QLabel()
        self.vault_mplus_value = QLabel()

        vault_grid.addWidget(self.vault_delves_name, 0, 0)
        vault_grid.addWidget(self.vault_delves_value, 0, 1)
        vault_grid.addWidget(self.vault_raid_name, 1, 0)
        vault_grid.addWidget(self.vault_raid_value, 1, 1)
        vault_grid.addWidget(self.vault_mplus_name, 2, 0)
        vault_grid.addWidget(self.vault_mplus_value, 2, 1)
        
        vault_grid.setColumnStretch(0, 1)
        vault_grid.setColumnStretch(1, 0)

        tiles_row.addWidget(self.vault_tile, 1)

    def set_character(self, character):

        self.pve_title.setText(f"<h3>{get_ui_string('pve')}</h3>")
        self.mplus_tile_title.setText(get_ui_string("mythic_plus"))

        self.vault_tile_title.setText(get_ui_string("vault"))
        self.vault_delves_name.setText(get_ui_string("delves"))

        self.vault_raid_name.setText(get_ui_string("raid"))
        self.vault_mplus_name.setText(get_ui_string("mythic_plus"))

        score = getattr(
            character,
            "mythic_score",
            None,
        )

        self.mythic_score_label.setText(str(score))

        self.mythic_score_label.setStyleSheet(
            f"""
            color: {get_mplus_color(score)};
            font-size: 28px;
            font-weight: bold;
            """
        )

        vault = load_user_vault(character)

        def dots(slots):

            result = []

            for index in range(3):

                if (
                    index < len(slots)
                    and slots[index]
                ):
                    result.append("●")

                else:
                    result.append("○")

            return " ".join(result)

        self.vault_delves_value.setText(dots(vault["row3"]))
        self.vault_raid_value.setText(dots(vault["row1"]))
        self.vault_mplus_value.setText(dots(vault["row2"]))