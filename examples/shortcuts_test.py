import flet as ft
import sys
import os

# Add the parent directory to sys.path to import from sibling packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flet_base.keyboard_shortcuts.shortcuts import ShortcutManager
from flet_base.config import DEFAULT_KEY_CONFIG

async def main(page: ft.Page):
    page.title = "Keyboard Shortcuts Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. Initialize manager
    manager = ShortcutManager()

    # 2. Register shortcuts directly from the global config dictionary
    manager.register_many(DEFAULT_KEY_CONFIG)

    # 3. UI
    status_label = ft.Text(
        "Press Mod+S or Mod+C to test", size=25, weight=ft.FontWeight.BOLD
    )

    # 4. Connect the manager to the page event
    page.on_keyboard_event = manager.handle_event

    page.add(
        ft.Icon(ft.Icons.KEYBOARD, size=100, color=ft.Colors.BLUE),
        status_label,
        ft.Text("Check the terminal for 'Hello' messages", color=ft.Colors.GREY_400),
    )


if __name__ == "__main__":
    ft.app(main)
