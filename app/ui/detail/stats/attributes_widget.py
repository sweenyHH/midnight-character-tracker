from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
)

from app.localization.ui_strings import get_ui_string
from app.services.display_language import get_display_language
from app.game_data.attribute_catalog import get_attribute_display_name


class AttributesWidget(QWidget):

    def _set_table_height(self, table, extra_padding=8):
        row_count = table.rowCount()

        header_height = (table.horizontalHeader().height())
        row_height = (table.verticalHeader().defaultSectionSize())
        total = (header_height + (row_height * row_count))
        table.setMinimumHeight(total + extra_padding)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(
                f"<b>{get_ui_string('primary_attributes')}</b>"
            )
        )

        self.attr_table = QTableWidget()

        self.attr_table.verticalHeader().setVisible(False)

        self.attr_table.setColumnCount(2)

        self.attr_table.setHorizontalHeaderLabels(
            [
                get_ui_string(
                    "attribute"
                ),
                get_ui_string(
                    "value"
                ),
            ]
        )

        layout.addWidget(
            self.attr_table
        )

    def set_character(
        self,
        character,
    ):

        attrs = getattr(
            character,
            "attributes",
            {},
        )

        self.attr_table.setRowCount(len(attrs))

        language = (get_display_language())

        for row, (k, v) in enumerate(attrs.items()):

            display_name = (get_attribute_display_name(k, language))
            attr_item = (QTableWidgetItem(display_name))
            font = attr_item.font()
            font.setBold(True)
            attr_item.setFont(font)

            self.attr_table.setItem(
                row,
                0,
                attr_item,
            )

            self.attr_table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(v)
                ),
            )

        self.attr_table.verticalHeader().setDefaultSectionSize(30)
        self.attr_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self._set_table_height(self.attr_table, extra_padding=12)
        self.attr_table.setMaximumHeight(self.attr_table.minimumHeight())

        header = (self.attr_table.horizontalHeader())
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)