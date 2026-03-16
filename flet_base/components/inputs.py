import datetime
import flet as ft
from flet_color_pickers import ColorPicker

from flet_base.themes.themes import instance_themes as themes


def switch(label, on_change=None, value=False, enabled=True):
    """It creates a switch with the specified label and change
    event handler and the main color of the theme"""
    return ft.Switch(
        label=label,
        on_change=on_change,
        value=value,
        disabled=not enabled,
        active_color=themes.actual_theme["primary"],
    )


def text_input(
    placeholder,
    on_change=None,
    value="",
    enabled=True,
    is_password=False,
    max_length=None,
    multiline=False,
    max_lines=1,
):
    """It creates a text input with autocomplete functionality.
    The autocomplete options can be easily modified to fit your needs."""
    return ft.TextField(
        label=placeholder,
        on_change=on_change,
        disabled=not enabled,
        value=value,
        password=is_password,
        can_reveal_password=is_password,
        max_length=max_length,
        multiline=multiline,
        max_lines=max_lines,
    )


def checkbox(label, on_change=None, value=False, enabled=True):
    """It creates a checkbox with the specified label and change
    event handler and the main color of the theme"""
    return ft.Checkbox(
        label=label,
        on_change=on_change,
        value=value,
        disabled=not enabled,
        active_color=themes.actual_theme["primary"],
    )


def color_picker(on_change=None, color="#FFFFFF"):
    """It creates a color picker with the specified label and
    change event handler and the main color of the theme"""
    return ColorPicker(on_color_change=on_change, color=color)


def date_picker(
    on_change=None,
    value=datetime.date.today(),
    first_date=datetime.date(1900, 1, 1),
    last_date=datetime.date.today(),
):
    """It creates a date picker with the specified label and change
    event handler and the main color of the theme"""
    return ft.DateRangePicker(
        on_change=on_change, first_date=first_date, last_date=last_date
    )


def date_range_picker(
    on_change=None,
    first_date=datetime.date(1900, 1, 1),
    last_date=datetime.date.today(),
    modal=True,
):
    """It creates a date range picker with the specified label and change
    event handler and the main color of the theme"""
    return ft.DateRangePicker(
        on_change=on_change,
        first_date=first_date,
        last_date=last_date,
        modal=modal,
        barrier_color=themes.actual_theme["background"],
    )


def time_picker(
    value=datetime.time(hour=19, minute=30),
    on_change=None,
    confirm_text="OK",
    error_invalid_text="Time out of range",
    help_text="Pick your time slot",
):
    """It creates a time picker with the specified label and change
    event handler and the main color of the theme"""
    return ft.TimePicker(
        value=value,
        confirm_text=confirm_text,
        error_invalid_text=error_invalid_text,
        help_text=help_text,
        entry_mode=ft.TimePickerEntryMode.DIAL,
        on_change=on_change,
    )


def dropdown(label, options, on_change=None, value=None):
    """It creates a dropdown with the specified label and change
    event handler and the main color of the theme. The options must be a list of DropdownOption objects."""
    return ft.Dropdown(
        label=label,
        options=options,
        on_select=on_change,
        value=value,
        color=themes.actual_theme["text_color"],
    )


def slider(label, on_change=None, value=0, min=0, max=100, divisions=50, enabled=True):
    """It creates a slider with the specified label and change
    event handler and the main color of the theme"""
    return ft.Slider(
        label=label,
        on_change=on_change,
        value=value,
        min=min,
        max=max,
        divisions=divisions,
        active_color=themes.actual_theme["primary"],
        inactive_color=themes.actual_theme["on_primary"],
    )
