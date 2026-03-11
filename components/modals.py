import flet as ft


from components.texts import title
from components.buttons import filled_btn
from themes.themes import instance_themes as themes


def bottom_sheet(content, width=700):
    """It creates a bottom sheet with the specified content and the main color of the theme"""
    return ft.BottomSheet(
        dismissible=True,
        bgcolor=themes.actual_theme["surface"],
        content=ft.Container(
            content=ft.Column(
                controls=content,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=width,
            padding=20,
        ),
    )


def modal(
    title_str,
    content,
    on_dismiss=None,
    width=700,
    actions=[filled_btn("Close", on_click=lambda e: e.control.page.pop_dialog())],
) -> ft.AlertDialog:
    """It creates a modal with the specified content and the main color of the theme"""
    return ft.AlertDialog(
        modal=True,
        title=title(title_str),
        content=ft.Container(
            content=ft.Column(
                controls=content,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            width=width,
        ),
        actions=actions,
        on_dismiss=on_dismiss,
        bgcolor=themes.actual_theme["surface"],
    )
