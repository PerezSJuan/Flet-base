import os
import sys
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from components.buttons import *
from themes.themes import instance_themes as themes


async def main(page):
    await themes.awake(page)
    
    page.add(
        ft.ListView(
            controls=[
                filled_btn("Filled Button"),
                icon_filled_btn(ft.Icons.FAVORITE),
                icon_btn(ft.Icons.INFO),
                text_btn("Text Button"),
                btn("Custom Colors"),
            ]
        )
    )


ft.run(main)
