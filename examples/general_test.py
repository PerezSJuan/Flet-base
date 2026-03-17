import os
import sys

# Allow running from the project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import flet as ft
import flet_base.router as fr
from flet_base.config import flet_config
from flet_base.translations import instance_translation_manager as tm
from flet_base.themes import instance_themes as themes
import flet_base.components.buttons as btn
import flet_base.components.texts as txt
import flet_base.components.data_display as dd
import flet_base.components.inputs as inputs

# ======================================================
# GLOBAL CONFIGURATION
# ======================================================

flet_config.translations_csv_path = os.path.join(os.path.dirname(__file__), "translations.csv")
flet_config.default_theme_mode = "light"

# ======================================================
# CREATE THE ROUTER
# ======================================================

app = fr.FletRouter(
    route_init="/home",
)

# ======================================================
# MIDDLEWARE & SHELLS
# ======================================================

@app.middleware
async def init_systems(data: fr.DataSystem):
    """Initializes themes and translations systems."""
    await tm.awake(data.page)
    await themes.awake(data.page)
    return fr.MiddlewareResult.next()

@app.shell()
def main_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
    """Global shell with Navigation Controls."""

    # Theme toggle icon
    theme_icon = ft.Icons.DARK_MODE if themes.actual_theme == themes.light_theme else ft.Icons.LIGHT_MODE

    async def toggle_theme(_):
        await themes.switch_theme(data.page)
        # Re-build the view to apply new theme colors to all components
        data.page.go(data.page.route)

    async def change_lang(e):
        code = tm.get_language_code(e.data)
        await tm.set_language(code, data.page)
        # Force the router to re-build the current view with new translations
        data.page.go(data.page.route)

    view.appbar = ft.AppBar(
        title=txt.title("Flet-base Demo", size=20),
        bgcolor=themes.actual_theme["surface"],
        actions=[
            ft.IconButton(theme_icon, on_click=toggle_theme),
            inputs.dropdown(
                label="Language",
                options=[ft.dropdown.Option(lang) for lang in tm.get_available_languages()],
                value=tm.get_language_name(tm.active_lang),
                on_change=change_lang,
            ),
        ]
    )
    return view

# ======================================================
# PAGE 1: HOME
# ======================================================

@app.page("/home", title="Home")
def home_page(data: fr.DataSystem) -> ft.View:
    return ft.View(
        route="/home",
        controls=[
            txt.title_primary(tm.translate("welcome")),
            txt.body(f"Current language: {tm.get_language_name(tm.active_lang)}"),
            dd.card(
                content=[
                    txt.subtitle("Package Highlights"),
                    txt.body("- Router-based navigation\n- Theme Management\n- I18n support\n- Premium Components"),
                ]
            ),
            btn.filled_btn(tm.translate("settings"), icon=ft.Icons.SETTINGS, on_click=lambda _: data.page.go("/about")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# ======================================================
# PAGE 2: ABOUT (Used as Settings here)
# ======================================================

@app.page("/about", title="About / Settings")
def about_page(data: fr.DataSystem) -> ft.View:
    return ft.View(
        route="/about",
        controls=[
            txt.title_secondary(tm.translate("settings")),
            dd.icon(ft.Icons.INFO_OUTLINE, size=50),
            dd.progress_bar(value=0.5),
            txt.body("This page demonstrates more components and translated text."),
            btn.text_btn(tm.translate("goodbye"), on_click=lambda _: data.page.go("/home")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# ======================================================
# 404 PAGE
# ======================================================

@app.page_404
def not_found(data: fr.DataSystem) -> ft.View:
    return ft.View(
        route="/404",
        controls=[
            txt.error_text("404 - Page Not Found", size=30),
            btn.filled_btn("Go Home", on_click=lambda _: data.page.go("/home")),
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# ======================================================
# RUN THE APP
# ======================================================

if __name__ == "__main__":
    app.run()