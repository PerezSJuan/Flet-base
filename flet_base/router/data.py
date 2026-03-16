"""
Data: the object passed to each page with access to navigation,
shared data, route parameters, and utilities.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable

import flet as ft

if TYPE_CHECKING:
    from .router import FletRouter


class DataSystem:
    """
    Object passed to each page function with access to:
    - page: the Flet ft.Page instance
    - route_params: parameters captured from dynamic routes (/user/:id)
    - query_params: query string parameters (?foo=bar)
    - shared: shared data between pages (persists in the session)
    - go(): navigates to a route
    - go_back(): returns to the previous route
    - history: history of visited routes
    """

    def __init__(
        self,
        page: ft.Page,
        router: "FletRouter",
        route_params: dict[str, str] | None = None,
        query_params: dict[str, str] | None = None,
    ):
        self.page_instance = page
        self.router_instance = router
        self.route_params_dict = route_params or {}
        self.query_params_dict = query_params or {}

        # Shared state persists between navigations in the same session
        if not hasattr(page, "_fr_shared"):
            page._fr_shared = {}  # type: ignore[attr-defined]

        # Navigation history
        if not hasattr(page, "_fr_history"):
            page._fr_history = []  # type: ignore[attr-defined]

    # ──────────────────────────────────────────────
    # Main properties
    # ──────────────────────────────────────────────

    @property
    def page(self) -> ft.Page:
        """The Flet ft.Page instance."""
        return self.page_instance

    @property
    def route_params(self) -> dict[str, str]:
        """Parameters captured from the dynamic route. E.g.: /user/42 → {'id': '42'}"""
        return self.route_params_dict

    @property
    def query_params(self) -> dict[str, str]:
        """Query string parameters. E.g.: ?tab=settings → {'tab': 'settings'}"""
        return self.query_params_dict

    @property
    def shared(self) -> dict[str, Any]:
        """
        Shared dictionary that persists throughout the user session.
        Use it to pass data between pages (e.g., authenticated user, cart, etc.)
        """
        return self.page_instance._fr_shared  # type: ignore[attr-defined]

    @property
    def history(self) -> list[str]:
        """History of routes visited in this session."""
        return self.page_instance._fr_history  # type: ignore[attr-defined]

    # ──────────────────────────────────────────────
    # Navigation
    # ──────────────────────────────────────────────

    def go(self, route: str, **kwargs: Any) -> Callable:
        """
        Returns an event handler that navigates to the indicated route.
        Usage: ft.ElevatedButton("Go", on_click=data.go("/home"))

        Also accepts extra parameters that are stored in shared before navigating:
            data.go("/profile", user_id=42)
        """
        def _handler(e: Any = None) -> None:
            if kwargs:
                self.page_instance._fr_shared.update(kwargs)  # type: ignore[attr-defined]
            self.page_instance.go(route)

        return _handler

    def go_back(self, e: Any = None) -> None:
        """
        Returns to the previous route in the history.
        If there is no history, it does nothing.
        """
        history: list[str] = self.page_instance._fr_history  # type: ignore[attr-defined]
        if len(history) >= 2:
            # The last element is the current route, the previous one is the destination
            target = history[-2]
            history.pop()  # remove current
            history.pop()  # remove target so go() can add it back
            self.page_instance.go(target)

    def redirect(self, route: str) -> None:
        """
        Redirects immediately to another route (useful within middleware).
        Unlike go(), it doesn't return a handler: it executes the navigation immediately.
        """
        self.page_instance.go(route)

    # ──────────────────────────────────────────────
    # Utilities
    # ──────────────────────────────────────────────

    def param(self, key: str, default: Any = None) -> Any:
        """
        Gets a dynamic route parameter with an optional default value.
        E.g.: data.param('id') in the route /user/:id
        """
        return self.route_params_dict.get(key, default)

    def query(self, key: str, default: Any = None) -> Any:
        """
        Gets a query string parameter with an optional default value.
        E.g.: data.query('tab') for ?tab=settings
        """
        return self.query_params_dict.get(key, default)

    def __repr__(self) -> str:
        return (
            f"<DataSystem route={self.page_instance.route!r} "
            f"params={self.route_params_dict} "
            f"query={self.query_params_dict}>"
        )
