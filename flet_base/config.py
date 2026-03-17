from typing import Optional, Dict

class FletBaseConfig:
    """
    Global configuration object for Flet-base.
    Modify these attributes from your main script before initializing components 
    to configure the package globally.
    """
    def __init__(self):
        # --- Translations Configuration ---
        # Provide an absolute path to your custom translations CSV here.
        # If None, the default internal translations.csv will be used.
        self.translations_csv_path: Optional[str] = None
        self.translations_csv_separator: str = ","
        self.default_language: str = "en"
        
        # --- Themes Configuration ---
        # Override the default themes dictionary by assigning to these variables.
        self.light_theme_override: Optional[Dict[str, str]] = None
        self.dark_theme_override: Optional[Dict[str, str]] = None
        self.default_theme_mode: str = "light"  # "light" or "dark"

        # --- Layout Configuration ---
        self.default_layout_spacing: int = 10
        self.default_layout_threshold: int = 600

# Global instance to be imported and modified by the user
flet_config = FletBaseConfig()
