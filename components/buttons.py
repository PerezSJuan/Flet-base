import flet as ft


from themes.themes import instance_themes as themes


def filled_btn(text, icon=None, on_click=None, enabled=True):
    """It creates a filled button with the specified text and click
    event handler and the main color of the theme"""
    return ft.FilledButton(
        content=text,
        icon=icon,
        on_click=on_click,
        bgcolor=themes.actual_theme["primary"],
        color=themes.actual_theme["on_primary"],
        disabled=not enabled,
    )


def icon_filled_btn(icon, on_click=None, enabled=True):
    """It creates a filled button with the specified icon and click
    event handler and the main color of the theme"""
    return ft.FilledIconButton(
        icon=icon,
        on_click=on_click,
        bgcolor=themes.actual_theme["primary"],
        icon_color=themes.actual_theme["on_primary"],
        disabled=not enabled,
    )


def icon_btn(icon, on_click=None, enabled=True):
    """It creates a empty button with the specified icon and click
    event handler and the main color of the theme"""
    return ft.IconButton(
        icon=icon,
        on_click=on_click,
        disabled=not enabled,
        icon_color=themes.actual_theme["primary"],
    )


def text_btn(text, icon=None, on_click=None, enabled=True):
    """It creates a empty (no bg) button with the specified text
    and the option of an icon and click event handler and the main
    color of the theme"""
    return ft.Button(
        content=text,
        icon=icon,
        on_click=on_click,
        color=themes.actual_theme["text_color"],
        disabled=not enabled,
    )


def btn(
    text,
    icon=None,
    on_click=None,
    enabled=True,
    light_bgcolor="#FFFFFF",
    light_color="#000000",
    dark_bgcolor="#121212",
    dark_color="#FFFFFF",
):
    """It creates a empty button with the specified text and the
    option of an icon and click event handler and choosen color"""
    bgcolor = (
        light_bgcolor if themes.actual_theme == themes.light_theme else dark_bgcolor
    )
    color = light_color if themes.actual_theme == themes.light_theme else dark_color
    return ft.FilledButton(
        content=text,
        icon=icon,
        on_click=on_click,
        bgcolor=bgcolor,
        color=color,
        disabled=not enabled,
    )
