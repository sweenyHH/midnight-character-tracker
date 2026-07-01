
# Entry point of the application. Initializes the Qt application, starts the main window.


import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.ui.theme_manager import ThemeManager


def main():

# Create the Qt application instance

    app = QApplication(sys.argv)

# Load dark theme stylesheet

    ThemeManager.load_theme(app, "dark")

# Create and show main window

    window = MainWindow()
    window.show()

# Start application event loop

    sys.exit(app.exec())

if __name__ == "__main__":
    main()