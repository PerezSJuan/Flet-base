import flet as ft
from flet_base.config import flet_config

class themes:
    """Helper class that manages light/dark theme switching."""

    actual_theme = None

    def __init__(self, default_theme=None):
        self.light_theme = flet_config.light_theme
        self.dark_theme = flet_config.dark_theme
        
        # Apply overrides if provided in config
        if flet_config.light_theme_override:
            self.light_theme.update(flet_config.light_theme_override)
        if flet_config.dark_theme_override:
            self.dark_theme.update(flet_config.dark_theme_override)
        
        if default_theme is None:
            mode = flet_config.default_theme_mode
            default_theme = self.dark_theme if mode == "dark" else self.light_theme
            
        self.default_theme = default_theme
        self.actual_theme = default_theme
        
    def _apply_typography(self, page):
        page.fonts = flet_config.font_files.copy()
        if flet_config.main_font_family:
            page.theme = ft.Theme(font_family=flet_config.main_font_family)
            page.dark_theme = ft.Theme(font_family=flet_config.main_font_family)

    async def set_dark_theme(self, page):
        page.theme_mode = ft.ThemeMode.DARK
        self.actual_theme = self.dark_theme
        self._apply_typography(page)
        await ft.SharedPreferences().set("theme", "dark")
        page.bgcolor = self.actual_theme["background"]
        page.update()

    async def set_light_theme(self, page):
        page.theme_mode = ft.ThemeMode.LIGHT
        self.actual_theme = self.light_theme
        self._apply_typography(page)
        await ft.SharedPreferences().set("theme", "light")
        page.bgcolor = self.actual_theme["background"]
        page.update()

    async def switch_theme(self, page):
        if self.actual_theme == self.light_theme:
            await self.set_dark_theme(page)
        elif self.actual_theme == self.dark_theme:
            await self.set_light_theme(page)
        else:
            await self.awake(page)

    async def awake(self, page):
        stored_theme = await ft.SharedPreferences().get("theme")

        if stored_theme == "dark":
            await self.set_dark_theme(page)
        elif stored_theme == "light":
            await self.set_light_theme(page)
        else:
            try:
                if page.platform_brightness == ft.Brightness.DARK:
                    await self.set_dark_theme(page)
                else:
                    await self.set_light_theme(page)
            except Exception:
                if self.default_theme == self.dark_theme:
                    await self.set_dark_theme(page)
                else:
                    await self.set_light_theme(page)


instance_themes = themes()
