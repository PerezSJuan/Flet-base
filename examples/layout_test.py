"""
layout_test.py

Example usage of ResponsiveAutoLayout (demo app).
Run with: flet run examples/layout_test.py
Requires Flet >= 0.80.0
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

    cards = [
        _make_card(ft.Colors.AMBER_200,       ft.Icons.DASHBOARD,      "Dashboard",   "Summary",   w=160,  h=130),
        _make_card(ft.Colors.LIGHT_GREEN_200, ft.Icons.PERSON,          "Users",       "Active",    w=320,  h=130),
        _make_card(ft.Colors.CYAN_200,        ft.Icons.SHOP,            "Sales",       "Today",     w=160,  h=130),
        _make_card(ft.Colors.PINK_200,        ft.Icons.SETTINGS,        "Settings",    "System",    w=600,  h=150),
        _make_card(ft.Colors.BLUE_200,        ft.Icons.MESSAGE,         "Messages",    "10 new",    w=240,  h=130),
        _make_card(ft.Colors.PURPLE_200,      ft.Icons.CALENDAR_TODAY,  "Events",      "Upcoming",  w=160,  h=130),
        _make_card(ft.Colors.ORANGE_200,      ft.Icons.STAR,            "Favorites",   "Bookmarked", w=1100, h=160),
        _make_card(ft.Colors.LIME_200,        ft.Icons.INSIGHTS,        "Analytics",   "Visits",    w=280,  h=130),
    ]

    info_text = ft.Text("", size=14)
    ral = ResponsiveAutoLayout(content=cards, page=page, threshold=0)

    page.add(
        ft.Column(
            controls=[
                ft.Row(controls=[info_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ral.control,
            ],
            spacing=12,
        )
    )

    def update_indicator(e):
        w = page.width or 0
        mode = "column" if w < ral.threshold else "row"
        page_padding = page.padding
        if isinstance(page_padding, (int, float)):
            total_padding = page_padding * 2
        else:
            try:
                total_padding = (page_padding.left or 0) + (page_padding.right or 0)
            except Exception:
                total_padding = 48
        available = max(0, w - total_padding)
        info_text.value = (
            f"page.width = {w:.0f}px — threshold = {ral.threshold}px "
            f"— mode = {mode} — available = {available:.0f}px"
        )
        try:
            info_text.update()
        except Exception:
            pass

    def on_resize_combined(e):
        ral._on_resize(e)
        update_indicator(e)

    page.on_resize = on_resize_combined
    update_indicator(None)
    ral._on_resize(None)


if __name__ == "__main__":
    ft.run(main)