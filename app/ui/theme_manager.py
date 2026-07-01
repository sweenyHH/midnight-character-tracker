import os


class ThemeManager:

    THEMES = {
        "dark": "assets/dark_theme.qss",
        "wow": "assets/wow_theme.qss",
        "modern": "assets/modern_theme.qss",
        "light": "assets/light_theme.qss",
    }

    current_theme = "dark"

    @classmethod
    def load_theme(cls, app, theme_name):

        if theme_name not in cls.THEMES:
            print(f"[ThemeManager] Unknown theme: {theme_name}")
            return

        path = cls.THEMES[theme_name]

        if not os.path.exists(path):
            print(f"[ThemeManager] Missing theme file: {path}")
            return

        with open(path, encoding="utf-8") as f:
            app.setStyleSheet(f.read())

        cls.current_theme = theme_name
        print(f"[ThemeManager] Loaded theme: {theme_name}")