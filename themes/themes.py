import flet as ft

light_theme = {
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
    "text_color": "#FFFFFF",
    "error": "#CF6679",
    "on_error": "#000000",
    "warning": "#FFB300",
    "success": "#66BB6A",
}


class themes:
    """Helper class that manages light/dark theme switching."""

    actual_theme = None

    def __init__(self, default_theme=light_theme):
        self.light_theme = light_theme
        self.dark_theme = dark_theme
        self.default_theme = default_theme
        self.actual_theme = default_theme

    async def set_dark_theme(self, page):
        page.theme_mode = ft.ThemeMode.DARK
        self.actual_theme = self.dark_theme
        await page.shared_preferences.set("theme", "dark")
        page.update()

    async def set_light_theme(self, page):
        page.theme_mode = ft.ThemeMode.LIGHT
        self.actual_theme = self.light_theme
        await page.shared_preferences.set("theme", "light")
        page.update()

    async def switch_theme(self, page):
        if self.actual_theme == self.light_theme:
            await self.set_dark_theme(page)
        elif self.actual_theme == self.dark_theme:
            await self.set_light_theme(page)
        else:
            await self.awake(page)

    async def awake(self, page):
        stored_theme = await page.shared_preferences.get("theme")

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