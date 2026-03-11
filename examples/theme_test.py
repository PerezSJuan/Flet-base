"""Standalone example demonstrating themes manager usage.

This script mirrors the translation example and shows how to toggle light
and dark palettes.  It lives in `examples/` and assumes the workspace root
is added to `sys.path` so the `themes` package/module can be imported.
"""

import flet as ft

from themes.themes import instance_themes as themes


async def main(page):
    await themes.awake(page)

    txt = ft.Text("The quick brown fox", size=24, color=themes.actual_theme["primary"])
    print(f"Initial theme: {themes.actual_theme['primary']}")

    async def toggle(_):

        await themes.switch_theme(page)
        # reflect current palette in our text color
        txt.color = themes.actual_theme["primary"]
        print(f"Switched to {themes.actual_theme['primary']} theme")

    page.add(
        txt,
        ft.Button("Toggle theme", on_click=toggle),
    )


if __name__ == "__main__":
    import flet as ft

    ft.app(target=main)
