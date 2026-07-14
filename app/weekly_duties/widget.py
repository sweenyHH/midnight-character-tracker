from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGridLayout, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt, QTimer

from app.ui.colors import STATUS_COLORS

from .config import ROWS_CONFIG

from app.utils.logger import logger

from app.storage.weekly_duties_storage import (
    load_state,
    save_state,
)

import os


class WeeklyDutiesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("<b>Weekly Duties</b>"))

        self.rows_config = ROWS_CONFIG

        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(12)
        self.grid.setVerticalSpacing(6)

        self.layout.addLayout(self.grid)
        self.layout.addStretch()

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all)
        self.layout.addWidget(self.clear_btn)

        self.current_file = None
        self.checkboxes = []
        self.row_labels = []

# Debounced saving
        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._save)

# Style checkboxes (green when checked)
        self.setStyleSheet(f"""
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
        }}

        QCheckBox::indicator:checked {{
            background-color: {STATUS_COLORS['success']};
            border: 1px solid {STATUS_COLORS['success']};
        }}

        QCheckBox::indicator:unchecked {{
            border: 1px solid #888;
            background: transparent;
        }}
        """)

# --------------------------------------------------
    def _schedule_save(self):
        self.save_timer.start(3000)

# --------------------------------------------------
    def _save(self):

        if not self.current_file:

            logger.warning(
                "Weekly duties save skipped: "
                "no character loaded"
            )

            return
        

        try:

            save_state(
                self.current_file,
                self.checkboxes
            )

            logger.info(
                f"Weekly duties saved: "
                f"{self.current_file}"
            )

        except Exception:

            logger.exception(
                f"Failed to save weekly duties: "
                f"{os.path.basename(self.current_file)}"
            )

            raise

# --------------------------------------------------
    def _update_row_visuals(self):

        for (row_index, boxes), label in zip(self.checkboxes, self.row_labels):

# reset style
            label.setStyleSheet("")

            checked = sum(1 for cb in boxes if cb.isChecked())
            total = len(boxes)

            if checked == total:
                style = f"color: {STATUS_COLORS['success']}; font-weight: bold;"
            else:
                style = f"color: {STATUS_COLORS['error']};"

            label.setStyleSheet(style)

# --------------------------------------------------
    def set_character(self, character):

        logger.info(
            f"Weekly duties loaded for: "
            f"{character.name}"
        )

        self.current_file = character.source_file
        self.row_labels = []

# clear grid properly
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.checkboxes.clear()

        try:

            saved_state = load_state(
                self.current_file
            )

        except Exception:

            logger.exception(
                f"Failed to load weekly duties: "
                f"{self.current_file}"
            )

            raise

        current_row = 0
        max_boxes = max(count for _, count in self.rows_config)

        for row_index, (name, count) in enumerate(self.rows_config):

# spacer row
            if name == "__SPACER__":
                spacer = QLabel("")
                spacer.setFixedHeight(12)
                self.grid.addWidget(spacer, current_row, 0)
                current_row += 1
                continue

# label
            label = QLabel(f"<b>{name}</b>")
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            label.setStyleSheet("")

            self.grid.addWidget(label, current_row, 0)
            self.row_labels.append(label)

            boxes = []

            for col in range(max_boxes):

                if col < count:
                    cb = QCheckBox()

                    key = f"{row_index}_{col}"
                    if saved_state.get(key):
                        cb.setChecked(True)

                    cb.stateChanged.connect(self._save)
                    cb.stateChanged.connect(self._update_row_visuals)

                    self.grid.addWidget(cb, current_row, col + 1)
                    boxes.append(cb)

                else:
                    self.grid.addWidget(QLabel(""), current_row, col + 1)

            self.checkboxes.append((row_index, boxes))
            current_row += 1

        self.grid.setColumnStretch(0, 1)

        self._update_row_visuals()

# --------------------------------------------------

    def clear_all(self):

        logger.info(
            f"Weekly duties cleared: "
            f"{os.path.basename(self.current_file)}"
        )

        for _, boxes in self.checkboxes:
            for cb in boxes:
                cb.setChecked(False)

        self._schedule_save()