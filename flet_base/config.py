from typing import Optional, Dict, Callable

# --- Default Themes ---
DEFAULT_LIGHT_THEME = {
    "primary": "#6200EE",
    "on_primary": "#FFFFFF",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#FFFFFF",
    "on_background": "#000000",
    "surface": "#FFFFFF",
    "on_surface": "#000000",
    "text_color": "#000000",
    "error": "#B00020",
    "on_error": "#FFFFFF",
    "warning": "#FFB300",
    "success": "#388E3C",
    "link": "#0000FF",
}

DEFAULT_DARK_THEME = {
    "primary": "#BB86FC",
    "on_primary": "#000000",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#121212",
    "on_background": "#FFFFFF",
    "surface": "#1E1E1E",
    "on_surface": "#FFFFFF",
    "text_color": "#FFFFFF",
    "error": "#CF6679",
    "on_error": "#000000",
    "warning": "#FFB300",
    "success": "#66BB6A",
    "link": "#5252FF",
}


# --- Default Key Configuration ---
DEFAULT_KEY_CONFIG = {
    "mod+s": lambda: print("Hello from Save!"),
    "mod+c": lambda: print("Hello from Copy!"),
}


class FletBaseConfig:
    """
    Global configuration object for Flet-base.
    Modify these attributes from your main script before initializing components
    to configure the package globally.
    """

    def __init__(self):
        # --- Translations Configuration ---
        # [VITAL] Provide an absolute path to your custom translations CSV here.
        # This is required for the TranslationManager to work correctly.
        self.translations_csv_path: Optional[str] = None
        self.translations_csv_separator: str = ","
        self.default_language: str = "en"

        # --- Themes Configuration ---
        # The themes below are used as the base for the application styling.
        # Custom themes MUST follow this key structure as components rely on them.
        self.light_theme: Dict[str, str] = DEFAULT_LIGHT_THEME.copy()
        self.dark_theme: Dict[str, str] = DEFAULT_DARK_THEME.copy()

        # Backward compatibility / specific overrides
        self.light_theme_override: Optional[Dict[str, str]] = None
        self.dark_theme_override: Optional[Dict[str, str]] = None

        self.default_theme_mode: str = "light"  # "light" or "dark"

        # --- Keyboard Shortcuts Configuration ---
        self.keyboard_shortcuts: Dict[str, Callable] = DEFAULT_KEY_CONFIG

        # --- Typography Configuration ---
        # Map font aliases/families to local files or URLs accepted by Flet.
        # Example: {"Inter": "assets/fonts/Inter-Regular.ttf"}
        self.font_files: Dict[str, str] = {}
        # Main UI font family used across components.
        # If None, Flet's default font is used.
        self.main_font_family: Optional[str] = None

        # --- Layout Configuration ---
        self.default_layout_spacing: int = 10
        self.default_layout_threshold: int = 0


# Global instance to be imported and modified by the user
flet_config = FletBaseConfig()
