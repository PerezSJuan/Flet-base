"""Standalone example demonstrating themes manager usage.

This script mirrors the translation example and shows how to toggle light
and dark palettes.  It lives in `examples/` and assumes the workspace root
is added to `sys.path` so the `themes` package/module can be imported.
"""

import os
import sys
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from themes.themes import themes


def main(page):
    th = themes()
    th.awake(page)

    txt = ft.Text("The quick brown fox", size=24, color=th.actual_theme["primary"])

    def toggle(_):
        th.switch_theme(page)
        # reflect current palette in our text color
        txt.color = th.actual_theme["primary"]
        page.update()

    page.add(
        txt,
        ft.ElevatedButton("Toggle theme", on_click=toggle),
    )


if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)
