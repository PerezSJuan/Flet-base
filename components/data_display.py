import flet as ft
import flet_datatable2 as fdt


from themes.themes import instance_themes as themes


def datatable(
    columns, rows, on_row_click=None, width=400, height=300, show_checkbox_column=False
):
    """It creates a datatable with the specified columns and rows and the main color of the theme."""
    return fdt.DataTable2(
        show_checkbox_column=show_checkbox_column,
        expand=True,
        width=width,
        height=height,
        column_spacing=0,
        heading_row_color=themes.actual_theme["surface"],
        horizontal_margin=12,
        sort_ascending=True,
        bottom_margin=10,
        min_width=600,
        on_select_all=lambda e: print("All selected"),
        columns=columns,
        rows=rows,
    )


def icon(icon, color=None, size=24):
    """It creates an icon with the specified icon, color and size and the main color of the theme"""
    if color is None:
        color = themes.actual_theme["primary"]
    return ft.Icon(icon=icon, color=color, size=size)


def image(src, width=100, height=100, border_radius=5):
    """It creates an image with the specified source, width and height and the main color of the theme"""
    return ft.Image(src=src, width=width, height=height, border_radius=border_radius)


def progress_bar(value, width=200, height=10):
    """It creates a progress bar with the specified value, width and height and the main color of the theme"""
    return ft.ProgressBar(
        value=value,
        width=width,
        height=height,
        bgcolor=themes.actual_theme["surface"],
        color=themes.actual_theme["primary"],
    )


def loading_indicator(size=50):
    """It creates a loading indicator"""
    return ft.ProgressRing(
        width=size, height=size, color=themes.actual_theme["primary"]
    )


def expansion_panel(header, content=[], expanded=False):
    """It creates an expansion panel with the specified header and content and the main color of the theme"""
    return ft.ExpansionPanel(
        header=ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        header,
                        size=16,
                        color=themes.actual_theme["text_color"],
                    ),
                ]
            ),
            padding=16,  # Simplified padding
        ),
        content=ft.Container(
            content=ft.Column(
                controls=content,
                spacing=15,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.only(left=16, right=16, bottom=16),
        ),
        expanded=expanded,
        bgcolor=themes.actual_theme["surface"],
        can_tap_header=True,
    )


def card(content=[], color=None):
    """It creates a card with the main color of the theme and a shadow"""
    if color is None:
        color = themes.actual_theme["primary"]
    return ft.Card(
        bgcolor=color,
        content=ft.Container(
            width=400,
            padding=15,
            content=ft.Column(
                controls=content,
                spacing=20,
            ),
        ),
    )
