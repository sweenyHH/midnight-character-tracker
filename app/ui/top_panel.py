from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt


class TopPanel(QWidget):

    def __init__(self, select_cb, paste_cb, back_cb):
        super().__init__()

        layout = QHBoxLayout()

# LEFT BOX (buttons)

        left = QVBoxLayout()

        self.select_btn = QPushButton("Select Data Folder")
        self.select_btn.clicked.connect(select_cb)

        self.paste_btn = QPushButton("Paste Character Data")
        self.paste_btn.clicked.connect(paste_cb)

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(back_cb)
        self.back_btn.hide()

        left.addWidget(self.select_btn)
        left.addWidget(self.paste_btn)
        left.addWidget(self.back_btn)
        left.addStretch()

# RIGHT BOX (reputation)

        self.rep_layout = QVBoxLayout()

        layout.addLayout(left)
        layout.addLayout(self.rep_layout)

        self.setLayout(layout)

    def update_reputation(self, reputation_list):

# clear

        while self.rep_layout.count():
            item = self.rep_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not reputation_list:
            self.rep_layout.addWidget(QLabel("No reputation data available"))
            return

        title = QLabel("Reputation")
        title.setAlignment(Qt.AlignCenter)
        self.rep_layout.addWidget(title)

        renown = []
        normal = []

        for rep in reputation_list:
            if rep.rep_type == "renown":
                renown.append(rep)
            else:
                normal.append(rep)

        renown.sort(key=lambda r: r.name)
        normal.sort(key=lambda r: r.name)

# Layout columns

        row = QHBoxLayout()

        left = QVBoxLayout()
        left.addWidget(QLabel("Renown"))

        for rep in renown:
            left.addWidget(QLabel(f"{rep.name}: {rep.level}"))

        right = QVBoxLayout()
        right.addWidget(QLabel("Standard"))

        for rep in normal:
            if rep.current:
                txt = f"{rep.name}: {rep.level} ({rep.current}/{rep.maximum})"
            else:
                txt = f"{rep.name}: {rep.level}"
            right.addWidget(QLabel(txt))

        row.addLayout(left)
        row.addLayout(right)

        self.rep_layout.addLayout(row)