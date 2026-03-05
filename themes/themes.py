import flet as ft

prefs = ft.SharedPreferences()

# A simple palette object used by the application.  You can extend or
# modify these values as needed; keys correspond to Flet's theme
# properties (primary, secondary, error, background, surface, etc.).
light_theme = {
    "primary": "#6200EE",
    "on_primary": "#FFFFFF",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#FFFFFF",
    "on_background": "#000000",
    "surface": "#FFFFFF",
    "on_surface": "#000000",
    "error": "#B00020",
    "on_error": "#FFFFFF",
    "warning": "#FFB300",
    "success": "#388E3C",
}

dark_theme = {
    "primary": "#BB86FC",
    "on_primary": "#000000",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#121212",
    "on_background": "#FFFFFF",
    "surface": "#1E1E1E",
    "on_surface": "#FFFFFF",
    "error": "#CF6679",
    "on_error": "#000000",
    "warning": "#FFB300",
    "success": "#66BB6A",
}


class themes:
    """Helper class that manages light/dark theme switching.

    Attributes:
        actual_theme (dict): currently active color dictionary.
        light_theme (dict): reference to the module-level light theme.
        dark_theme (dict): reference to the module-level dark theme.
    """

    actual_theme = None

    def __init__(self, default_theme=light_theme):
        """Initialize the manager with a default theme.

        The provided default_theme should be either `light_theme` or
        `dark_theme`.  The instance keeps references to both palettes
        and sets `actual_theme` accordingly.
        """
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.default_theme = default_theme
        self.actual_theme = default_theme

    def set_dark_theme(self, page):
        """Apply the dark color palette to the given Flet page.

        This sets the page's theme_mode to `ThemeMode.DARK` and updates
        `actual_theme` so clients can read the current color values.
        """
        page.theme_mode = ft.ThemeMode.DARK
        self.actual_theme = self.dark_theme
        prefs.set("theme", "dark")

    def set_light_theme(self, page):
        """Apply the light color palette to the given Flet page.

        Unlike ``set_dark_theme``, this switches the page to
        `ThemeMode.LIGHT` and updates ``actual_theme`` accordingly.
        """
        page.theme_mode = ft.ThemeMode.LIGHT
        self.actual_theme = self.light_theme
        prefs.set("theme", "light")

    def switch_theme(self, page):
        """Toggle between light and dark themes.

        If the current palette matches `light_theme`, switch to dark, and
        vice versa.  If the active palette is somehow neither, fall back to
        `awake()` which chooses based on saved preferences or defaults.
        """
        if self.actual_theme == self.light_theme:
            self.set_dark_theme(page)
        elif self.actual_theme == self.dark_theme:
            self.set_light_theme(page)
        else: 
            self.awake(page)
    
    def awake(self, page):
        """Initialize theme on page creation.

        Reads the stored value from ``prefs`` under the
        key "theme".  If found, applies it; otherwise inspects
        ``ft.ThemeMode.SYSTEM`` and the ``default_theme`` provided at
        construction to choose a starting theme, then saves that choice.
        """
        stored_theme = prefs.get("theme")
        if stored_theme:
            if stored_theme == "light":
                self.set_light_theme(page)
            elif stored_theme == "dark":
                self.set_dark_theme(page)
        else:
            if ft.ThemeMode.SYSTEM == ft.ThemeMode.LIGHT:
                self.set_light_theme(page)
                
            elif ft.ThemeMode.SYSTEM == ft.ThemeMode.DARK:
                self.set_dark_theme(page)
            else: 
                if self.default_theme == self.light_theme:
                    self.set_light_theme(page)
                elif self.default_theme == self.dark_theme:
                    self.set_dark_theme(page)
                else:
                    self.set_light_theme(page)

