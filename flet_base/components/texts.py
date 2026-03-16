import flet as ft

from flet_base.themes.themes import instance_themes as themes


def markdown(md, size=12):
    """It creates a markdown text with the specified markdown content and the main color of the theme"""
    style = ft.MarkdownStyleSheet()
    style.p = ft.TextStyle(color=themes.actual_theme["text_color"], size=size)
    return ft.Markdown(
        value=md,
        selectable=True,
        md_style_sheet=style,
        latex_style=ft.TextStyle(color=themes.actual_theme["text_color"], size=size),
    )


def title(
    text: str,
    size: int = 24,
    color=None,
    weight=ft.FontWeight.BOLD,
    selectable: bool = True,
):
    """Title style text (large and bold by default)."""
    if color is None:
        color = themes.actual_theme["text_color"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def title_primary(
    text: str,
    size: int = 24,
    color=None,
    weight=ft.FontWeight.BOLD,
    selectable: bool = True,
):
    """Title style text using the primary theme color."""
    if color is None:
        color = themes.actual_theme["primary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def title_on_primary(
    text: str,
    size: int = 24,
    color=None,
    weight=ft.FontWeight.BOLD,
    selectable: bool = True,
):
    """Title style text using the 'on_primary' theme color."""
    if color is None:
        color = themes.actual_theme["on_primary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def title_secondary(
    text: str,
    size: int = 24,
    color=None,
    weight=ft.FontWeight.BOLD,
    selectable: bool = True,
):
    """Title style text using the secondary theme color."""
    if color is None:
        color = themes.actual_theme["secondary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def title_on_secondary(
    text: str,
    size: int = 24,
    color=None,
    weight=ft.FontWeight.BOLD,
    selectable: bool = True,
):
    """Title style text using the 'on_secondary' theme color."""
    if color is None:
        color = themes.actual_theme["on_secondary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def subtitle(
    text: str,
    size: int = 19,
    color=None,
    weight=ft.FontWeight.NORMAL,
    selectable: bool = True,
):
    """Subtitle style text (medium size and normal weight by default)."""
    if color is None:
        color = themes.actual_theme["text_color"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def subtitle_primary(
    text: str,
    size: int = 19,
    color=None,
    weight=ft.FontWeight.NORMAL,
    selectable: bool = True,
):
    """Subtitle style text using the primary theme color."""
    if color is None:
        color = themes.actual_theme["primary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def subtitle_secondary(
    text: str,
    size: int = 19,
    color=None,
    weight=ft.FontWeight.NORMAL,
    selectable: bool = True,
):
    """Subtitle style text using the secondary theme color."""
    if color is None:
        color = themes.actual_theme["secondary"]
    return ft.Text(text, size=size, color=color, weight=weight, selectable=selectable)


def body(
    text: str,
    size: int = 12,
    color=None,
    selectable: bool = True,
):
    """Body style text (standard normal text)."""
    if color is None:
        color = themes.actual_theme["text_color"]
    return ft.Text(text, size=size, color=color, selectable=selectable)


def caption(
    text: str,
    size: int = 12,
    color=None,
    italic: bool = False,
):
    """Small caption style text for notes or descriptions."""
    if color is None:
        color = themes.actual_theme["text_color"]
    return ft.Text(text, size=size, color=color, italic=italic)


def error_text(text: str, size: int = 12, weight=None):
    """Themed red text for error messages."""
    return ft.Text(text, size=size, color=themes.actual_theme["error"], weight=weight)


def success_text(text: str, size: int = 12, weight=None):
    """Themed green text for success messages."""
    return ft.Text(text, size=size, color=themes.actual_theme["success"], weight=weight)


def warning_text(text: str, size: int = 12, weight=None):
    """Themed yellow text for warning messages."""
    return ft.Text(text, size=size, color=themes.actual_theme["warning"], weight=weight)


async def link(url: str, page: ft.Page, text: str = None, size: int = 12):
    """Link style text."""
    if text is None:
        text = url

    async def on_click(e):
        await page.launch_url(url)

    return ft.TextButton(
        content=ft.Text(
            text,
            color=themes.actual_theme["link"],
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
            size=size,
        ),
        on_click=on_click,
    )
