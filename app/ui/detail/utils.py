from PySide6.QtWidgets import QVBoxLayout
from app.utils.number_formatter import format_number

def clear_layout(widget):
    layout = widget.layout()
    if not layout:
        return

    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()


def get_layout(widget):
    layout = widget.layout()

    if layout is None:
        layout = QVBoxLayout()
        widget.setLayout(layout)
    else:
        clear_layout(widget)

    return layout


def format_gold(copper):
    gold = copper // 10000
    silver = (copper % 10000) // 100
    copper_remainder = copper % 100

    parts = []
    if gold > 0:
        parts.append(
            f"{format_number(gold)}g"
        )
        
    if silver > 0:
        parts.append(f"{silver}s")
    if copper_remainder > 0:
        parts.append(f"{copper_remainder}c")

    return " ".join(parts) if parts else "0c"