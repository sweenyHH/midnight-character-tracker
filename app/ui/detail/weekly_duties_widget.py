from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QGridLayout, QCheckBox, QPushButton
)
from PySide6.QtCore import Qt
import os

from app.ui.colors import STATUS_COLORS


class WeeklyDutiesWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("<b>Weekly Duties</b>"))

        self.rows_config = [
            ("Gilded Stash", 4),
            ("Nightmare Hunt", 4),
            ("Radiant Spark Quest", 1),
            ("Nebulous Voidcore Quest", 1),

            ("__SPACER__", 0),

            ("Profession Treatsie", 2),
            ("Profession Quests", 2),
        ]

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

# --------------------------------------------------
    def _update_row_visuals(self):

        for (row_index, boxes), label in zip(self.checkboxes, self.row_labels):

# HARD RESET STYLE 
            label.setStyleSheet("")  

            checked = sum(1 for cb in boxes if cb.isChecked())
            total = len(boxes)

            if checked == 0:
                return_style = ""

            elif checked == total:
                return_style = f"color: {STATUS_COLORS['success']}; font-weight: bold;"

            else:
                return_style = f"color: {STATUS_COLORS['warning']};"

# APPLY ONLY AFTER RESET
            label.setStyleSheet(return_style)

# --------------------------------------------------

    def set_character(self, character):

        self.current_file = character.source_file
        self.row_labels = []

# CLEAN GRID PROPERLY
        while self.grid.count():
            item = self.grid.takeAt(0)

            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.checkboxes.clear()

        saved_state = self._load_state()

        current_row = 0
        max_boxes = max(count for _, count in self.rows_config)

        for row_index, (name, count) in enumerate(self.rows_config):

            if name == "__SPACER__":
                spacer = QLabel("")
                spacer.setFixedHeight(12)
                self.grid.addWidget(spacer, current_row, 0)
                current_row += 1
                continue

            label = QLabel(name)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

# ensure clean style
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

                    cb.stateChanged.connect(self._save_state)
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

        for _, boxes in self.checkboxes:
            for cb in boxes:
                cb.setChecked(False)

        self._save_state()

# --------------------------------------------------
    def _load_state(self):

        result = {}

        if not self.current_file or not os.path.exists(self.current_file):
            return result

        in_user_block = False
        in_section = False

        with open(self.current_file, encoding="utf-8") as f:
            for line in f:

                stripped = line.strip()

                if stripped == "### USER_DATA_START ###":
                    in_user_block = True
                    continue

                if stripped == "### USER_DATA_END ###":
                    break

                if in_user_block and stripped == "WeeklyDuties:":
                    in_section = True
                    continue

                if in_section:
                    if "=" in stripped:
                        k, v = stripped.split("=")
                        result[k] = (v == "1")
                    elif stripped.endswith(":"):
                        break

        return result

# --------------------------------------------------
    def _save_state(self):

        if not self.current_file or not os.path.exists(self.current_file):
            return

        with open(self.current_file, encoding="utf-8") as f:
            lines = f.readlines()

        in_user_block = False
        notes_lines = []
        new_lines = []

        for line in lines:

            stripped = line.strip()

            if stripped == "### USER_DATA_START ###":
                in_user_block = True
                continue

            if stripped == "### USER_DATA_END ###":
                in_user_block = False
                continue

            if in_user_block:
                if stripped.startswith("Notes:") or notes_lines:
                    notes_lines.append(line)
                    continue

                if stripped.startswith("WeeklyDuties:") or "=" in stripped:
                    continue

            else:
                new_lines.append(line)

        duty_lines = []

        for row_index, boxes in self.checkboxes:
            for i, cb in enumerate(boxes):
                if cb.isChecked():
                    duty_lines.append(f"{row_index}_{i}=1\n")

        user_block = []

        if notes_lines or duty_lines:
            user_block.append("### USER_DATA_START ###\n")

            if notes_lines:
                user_block.extend(notes_lines)

            if duty_lines:
                user_block.append("WeeklyDuties:\n")
                user_block.extend(duty_lines)

            user_block.append("### USER_DATA_END ###\n")

        with open(self.current_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

            if user_block:
                f.write("\n")
                f.writelines(user_block)