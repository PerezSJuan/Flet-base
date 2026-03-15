"""
layout_test.py

Ejemplo de uso de ResponsiveAutoLayout (demo app).
Usar con: flet run examples/layout_test.py
Requiere Flet >= 0.80.0
"""

import flet as ft
from layout.responsive_auto_layout import ResponsiveAutoLayout


def _make_card(color, icon, title, subtitle, w=160, h=130):
    return ft.Container(
        width=w,
        height=h,
        padding=12,
        bgcolor=color,
        border_radius=8,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            controls=[
                ft.Icon(icon, size=28),
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )


def main(page: ft.Page):
    page.title = "ResponsiveAutoLayout — demo"
    page.window_width = 900
    page.window_height = 600
    page.padding = 20

    tarjetas = [
        _make_card(ft.Colors.AMBER_200,       ft.Icons.DASHBOARD,      "Panel",      "Resumen",   w=160,  h=130),
        _make_card(ft.Colors.LIGHT_GREEN_200, ft.Icons.PERSON,          "Usuarios",   "Activos",   w=320,  h=130),
        _make_card(ft.Colors.CYAN_200,        ft.Icons.SHOP,            "Ventas",     "Hoy",       w=160,  h=130),
        _make_card(ft.Colors.PINK_200,        ft.Icons.SETTINGS,        "Ajustes",    "Sistema",   w=600,  h=150),
        _make_card(ft.Colors.BLUE_200,        ft.Icons.MESSAGE,         "Mensajes",   "10 nuevos", w=240,  h=130),
        _make_card(ft.Colors.PURPLE_200,      ft.Icons.CALENDAR_TODAY,  "Eventos",    "Próximos",  w=160,  h=130),
        _make_card(ft.Colors.ORANGE_200,      ft.Icons.STAR,            "Favoritos",  "Marcados",  w=1100, h=160),
        _make_card(ft.Colors.LIME_200,        ft.Icons.INSIGHTS,        "Analítica",  "Visitas",   w=280,  h=130),
    ]

    info = ft.Text("", size=14)
    ral = ResponsiveAutoLayout(content=tarjetas, page=page, threshold=0)

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[info], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ral.control,
            ],
            spacing=12,
        )
    )

    def actualizar_indicador(e):
        w = page.width or 0
        mode = "column" if w < ral.threshold else "row"
        page_pad = page.padding
        if isinstance(page_pad, (int, float)):
            pad = page_pad * 2
        else:
            try:
                pad = (page_pad.left or 0) + (page_pad.right or 0)
            except Exception:
                pad = 48
        available = max(0, w - pad)
        info.value = (
            f"page.width = {w:.0f}px — threshold = {ral.threshold}px "
            f"— mode = {mode} — available = {available:.0f}px"
        )
        try:
            info.update()
        except Exception:
            pass

    def on_resize_combinado(e):
        ral._on_resize(e)
        actualizar_indicador(e)

    page.on_resize = on_resize_combinado
    actualizar_indicador(None)
    ral._on_resize(None)


if __name__ == "__main__":
    ft.run(main)