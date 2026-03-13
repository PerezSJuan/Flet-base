import asyncio

import flet as ft


drawer_items = [
    ("Inicio", ft.Icons.HOME, "Abriendo inicio"),
    ("Proyectos", ft.Icons.VIEW_LIST, "Mostrando proyectos"),
    ("Favoritos", ft.Icons.STAR, "Favoritos cargados"),
    ("Ajustes", ft.Icons.SETTINGS, "Configuración lista"),
]


def _build_navigation_drawer(notify: ft.ControlEventHandler):
    def _handle_change(event):
        index = event.control.selected_index
        if index is None or index < 0:
            return
        _, _, message = drawer_items[index]
        notify(message)

    def _handle_dismiss(_event):
        notify("Drawer cerrado")

    return ft.NavigationDrawer(
        bgcolor=ft.Colors.WHITE,
        elevation=4,
        indicator_color=ft.Colors.INDIGO_400,
        tile_padding=ft.Padding.symmetric(vertical=6, horizontal=14),
        controls=[
            ft.NavigationDrawerDestination(icon=icon, label=label)
            for label, icon, _ in drawer_items
        ],
        on_change=_handle_change,
        on_dismiss=_handle_dismiss,
    )


def main(page: ft.Page):
    page.title = "Shell Topbar · Burger Drawer"
    page.window_width = 960
    page.window_height = 640
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_50

    snackbar = ft.SnackBar(content=ft.Text(""))
    page.snack_bar = snackbar

    def notify(message: str):
        snackbar.content.value = message
        snackbar.open = True
        page.update()
        asyncio.create_task(page.close_drawer())

    page.drawer = _build_navigation_drawer(lambda msg: notify(msg))

    async def toggle_drawer(_event):
        await page.show_drawer()

    page.appbar = ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=toggle_drawer),
        title=ft.Text("Topbar con Drawer", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.INDIGO_700,
        elevation=0,
        actions=[
            ft.IconButton(
                icon=ft.Icons.NOTIFICATIONS,
                tooltip="Notificaciones",
                icon_color=ft.Colors.WHITE,
                on_click=lambda _: notify("No hay alertas nuevas"),
            )
        ],
    )

    page.add(
        ft.Container(
            expand=True,
            padding=ft.Padding.symmetric(horizontal=32, vertical=28),
            content=ft.Column(
                [
                    ft.Text(
                        "Un menú lateral con navegación rápida",
                        size=26,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                    ft.Text(
                        "Presiona el botón hamburguesa para abrir el drawer, elegir una sección y ver feedback inmediato.",
                        size=16,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Row(
                        [
                            ft.Button(
                                content="Nuevo proyecto",
                                icon=ft.Icons.ADD,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.INDIGO_600,
                                    color=ft.Colors.WHITE,
                                    elevation=2,
                                ),
                                on_click=lambda _: notify("Proyecto inicializado"),
                            ),
                            ft.Button(
                                content="Compartir topbar",
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.WHITE,
                                    color=ft.Colors.INDIGO_700,
                                    side=ft.BorderSide(width=1, color=ft.Colors.INDIGO_200),
                                    elevation=0,
                                ),
                                on_click=lambda _: notify("Topbar compartido"),
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Divider(height=24),
                    ft.Row(
                        [
                            ft.Container(
                                expand=True,
                                padding=ft.Padding.symmetric(vertical=20, horizontal=18),
                                border_radius=12,
                                bgcolor=ft.Colors.WHITE,
                                content=ft.Column(
                                    [
                                        ft.Text("Estado de la bandeja", weight=ft.FontWeight.W_600),
                                        ft.Text("3 tareas pendientes"),
                                        ft.Text("2 aprobaciones necesarias"),
                                    ],
                                    spacing=6,
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                padding=ft.Padding.symmetric(vertical=20, horizontal=18),
                                border_radius=12,
                                bgcolor=ft.Colors.WHITE,
                                content=ft.Column(
                                    [
                                        ft.Text("Colabora rápido", weight=ft.FontWeight.W_600),
                                        ft.Text("Comparte vínculos seguros"),
                                        ft.Text("Control de accesos activo"),
                                    ],
                                    spacing=6,
                                ),
                            ),
                        ],
                        spacing=16,
                    ),
                ],
                spacing=18,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
