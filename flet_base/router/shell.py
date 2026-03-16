"""
ShellComponent: persistent UI components that are rendered
around the content of each page (AppBar, MenuBar, Drawer, etc.)

A Shell can be applied to all routes or only to a subset.

Example:
    @app.shell(routes=["/dashboard", "/settings", "/profile"])
    def main_shell(data: DataSystem, view: ft.View) -> ft.View:
        view.appbar = ft.AppBar(title=ft.Text("My App"))
        view.drawer = ft.NavigationDrawer(...)
        return view

    # Or with a route prefix:
    @app.shell(prefix="/admin")
    def admin_shell(data: DataSystem, view: ft.View) -> ft.View:
        view.appbar = ft.AppBar(title=ft.Text("Admin Panel"), bgcolor=ft.Colors.RED)
        return view
"""

from __future__ import annotations
from typing import Callable, Any


class ShellComponent:
    """
    Represents a shell component: a function that receives (data, view)
    and returns a modified ft.View with persistent elements.

    Route matching (in order of priority):
    1. routes=[...]: exact list of routes to apply
    2. prefix="...": all routes that start with that prefix
    3. If both are None/empty: applies to ALL routes (global shell)
    """

    def __init__(
        self,
        func: Callable,
        routes: list[str] | None = None,
        prefix: str | None = None,
        exclude: list[str] | None = None,
    ):
        self.func = func
        self.routes: list[str] = routes or []
        self.prefix: str | None = prefix
        self.exclude: list[str] = exclude or []

    def applies_to(self, route: str) -> bool:
        """Does this shell apply to the given route?"""
        # Exclusions first
        if route in self.exclude:
            return False

        # Exact matching
        if self.routes:
            return route in self.routes

        # Prefix matching
        if self.prefix:
            return route.startswith(self.prefix)

        # Global shell
        return True

    def apply(self, data: Any, view: Any) -> Any:
        """Applies the shell to the view, returns the modified view."""
        return self.func(data, view)

    def __repr__(self) -> str:
        return (
            f"<ShellComponent prefix={self.prefix!r} "
            f"routes={self.routes} exclude={self.exclude}>"
        )
