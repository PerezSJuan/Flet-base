import flet as ft


def _make_snackbar(page: ft.Page) -> ft.SnackBar:
    snack = ft.SnackBar(content=ft.Text(""))
    page.snack_bar = snack
    return snack


def main(page: ft.Page):
    page.title = "Shell Topbar · Windows"
    page.window_width = 1040
    page.window_height = 720
    page.padding = 0
    page.bgcolor = ft.Colors.GREY_200

    snackbar = _make_snackbar(page)

    def notify(message: str):
        snackbar.content.value = message
        snackbar.open = True
        page.snack_bar = snackbar
        page.update()

    menubar = ft.MenuBar(
        style=ft.MenuStyle(bgcolor=ft.Colors.WHITE),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("Archivo"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.CREATE_NEW_FOLDER),
                        content=ft.Text("Nuevo"),
                        on_click=lambda _: notify("Documento nuevo"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.FOLDER_OPEN),
                        content=ft.Text("Abrir..."),
                        on_click=lambda _: notify("Explorador abierto"),
                    ),
                    ft.Divider(),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.SAVE),
                        content=ft.Text("Guardar"),
                        on_click=lambda _: notify("Cambios guardados"),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Editar"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.CUT),
                        content=ft.Text("Cortar"),
                        on_click=lambda _: notify("Texto cortado"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.CONTENT_COPY),
                        content=ft.Text("Copiar"),
                        on_click=lambda _: notify("Texto copiado"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.PASTE),
                        content=ft.Text("Pegar"),
                        on_click=lambda _: notify("Texto pegado"),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Ver"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.ZOOM_IN),
                        content=ft.Text("Zoom +"),
                        on_click=lambda _: notify("Zoom aumentado"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.ZOOM_OUT),
                        content=ft.Text("Zoom -"),
                        on_click=lambda _: notify("Zoom reducido"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.FULLSCREEN),
                        content=ft.Text("Pantalla completa"),
                        on_click=lambda _: notify("Modo inmersivo activado"),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Ayuda"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.INFO),
                        content=ft.Text("Acerca de"),
                        on_click=lambda _: notify("Versión 1.0"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.HELP),
                        content=ft.Text("Documentación"),
                        on_click=lambda _: notify("Documentación abierta"),
                    ),
                ],
            ),
        ],
    )

    page.add(
        ft.Column(
            [
                menubar,
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.WHITE,
                    padding=ft.Padding.symmetric(horizontal=28, vertical=30),
                    content=ft.Column(
                        [
                            ft.Text(
                                "Topbar estilo Windows",
                                size=26,
                                weight=ft.FontWeight.W_600,
                                color=ft.Colors.GREY_900,
                            ),
                            ft.Text(
                                "El menú clásico (Archivo, Editar, Ver, Ayuda) se ancla sobre el contenido principal y guía los flujos interactivos.",
                                size=16,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Divider(height=24),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.DESKTOP_WINDOWS, size=56, color=ft.Colors.BLUE_600),
                                    ft.Text(
                                        "Utiliza cada opción del menú para comprobar que el shell responde con feedback rápido.",
                                        size=14,
                                        color=ft.Colors.GREY_600,
                                    ),
                                ],
                                spacing=16,
                            ),
                        ],
                        spacing=16,
                    ),
                ),
            ],
            spacing=0,
        )
    )


if __name__ == "__main__":
    ft.run(main)
