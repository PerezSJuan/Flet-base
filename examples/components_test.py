import os
import sys
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)


from components.buttons import filled_btn, icon_filled_btn, icon_btn, text_btn, btn
from components.data_display import (
    icon,
    image,
    progress_bar,
    loading_indicator,
    datatable,
)
import flet_datatable2 as fdt
from themes.themes import instance_themes as themes


async def main(page: ft.Page):
    await themes.awake(page)
    page.title = "Component Test"
    page.padding = 40
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "surface"

    async def toggle_theme(e):
        await themes.switch_theme(page)
        # Limpiamos y volvemos a ejecutar main para refrescar los componentes con los nuevos HEX
        page.controls.clear()
        await main(page)

    # Header
    page.add(
        ft.Row(
            [
                ft.Text(
                    "Component Library Test",
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    color=themes.actual_theme["primary"],
                ),
                ft.IconButton(
                    icon=ft.Icons.BRIGHTNESS_4,
                    on_click=toggle_theme,
                    icon_color=themes.actual_theme["primary"],
                ),
                ft.Button(
                    content="Toggle Theme",
                    on_click=toggle_theme,
                    color=themes.actual_theme["primary"],
                    bgcolor=themes.actual_theme["on_primary"],
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    # Define DataTable content
    columns = [
        fdt.DataColumn2(label=ft.Text("ID")),
        fdt.DataColumn2(label=ft.Text("Name")),
        fdt.DataColumn2(label=ft.Text("Role")),
    ]
    rows = [
        fdt.DataRow2(
            cells=[
                ft.DataCell(ft.Text("1")),
                ft.DataCell(ft.Text("Juan")),
                ft.DataCell(ft.Text("Developer")),
            ]
        ),
        fdt.DataRow2(
            cells=[
                ft.DataCell(ft.Text("2")),
                ft.DataCell(ft.Text("Perez")),
                ft.DataCell(ft.Text("Designer")),
            ]
        ),
        fdt.DataRow2(
            cells=[
                ft.DataCell(ft.Text("3")),
                ft.DataCell(ft.Text("Sanz")),
                ft.DataCell(ft.Text("Manager")),
            ]
        ),
    ]

    # Sections
    sections = [
        (
            "Buttons",
            [
                ft.Row(
                    [filled_btn("Filled Button"), icon_filled_btn(ft.Icons.FAVORITE)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [icon_btn(ft.Icons.INFO), text_btn("Text Button")],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row([btn("Custom Colors")], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
        (
            "Data Display",
            [
                ft.Row(
                    [icon(ft.Icons.FAVORITE, size=50)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [image("https://picsum.photos/200", width=150, height=150)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [progress_bar(0.7, width=300)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [loading_indicator(size=40)], alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
        ),
        ("DataTable", [datatable(columns=columns, rows=rows, width=600, height=300)]),
    ]

    content = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
        width=800,
    )

    for title, controls in sections:
        content.controls.append(ft.Text(title, size=24, weight=ft.FontWeight.BOLD))
        content.controls.append(
            ft.Container(
                content=ft.Column(
                    controls,
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                border_radius=10,
                bgcolor="surfaceVariant",
                border=ft.border.all(1, "outlineVariant"),
            )
        )

    page.add(
        ft.Row(
            [content],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.run(main)
