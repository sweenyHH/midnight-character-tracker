# Displays detailed information for a single character.


from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar


class DetailView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def set_character(self, character):
  
# Populates UI with character data.
  
# Clear previous widgets

        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

# Character name

        self.layout.addWidget(QLabel(f"Character: {character.name}"))

# Location info

        for key, value in character.location.items():
            self.layout.addWidget(QLabel(f"{key}: {value}"))

# Currency display

        for currency in character.currencies:
            label = QLabel(f"{currency.name}")
            self.layout.addWidget(label)

            if currency.max_value:
                progress = QProgressBar()
                progress.setMaximum(currency.max_value)
                progress.setValue(currency.quantity)
                self.layout.addWidget(progress)
            else:
                self.layout.addWidget(QLabel(f"Amount: {currency.quantity}"))