"""
Middleware system for FletRouter.

A middleware is a function that receives a DataSystem object and decides to:
- Continue (returning MiddlewareResult.next())
- Redirect (returning MiddlewareResult.redirect("/login"))
- Block with a custom view (returning MiddlewareResult.view(ft.View(...)))

Example:
    def auth_middleware(data: DataSystem) -> MiddlewareResult:
        if not data.shared.get("user"):
            return MiddlewareResult.redirect("/login")
        return MiddlewareResult.next()
"""

from __future__ import annotations
from typing import Any
import flet as ft


class MiddlewareResult:
    """Result that a middleware must return."""

    NEXT = "next"
    REDIRECT = "redirect"
    VIEW = "view"

    def __init__(self, action: str, target: Any = None):
        self.action = action
        self.target = target  # route string or ft.View

    @classmethod
    def next(cls) -> "MiddlewareResult":
        """Continue with normal navigation."""
        return cls(cls.NEXT)

    @classmethod
    def redirect(cls, route: str) -> "MiddlewareResult":
        """Redirect to another route."""
        return cls(cls.REDIRECT, target=route)

    @classmethod
    def view(cls, view: ft.View) -> "MiddlewareResult":
        """Show a custom view (blocking with own UI)."""
        return cls(cls.VIEW, target=view)

    @property
    def should_continue(self) -> bool:
        return self.action == self.NEXT

    @property
    def should_redirect(self) -> bool:
        return self.action == self.REDIRECT

    @property
    def has_view(self) -> bool:
        return self.action == self.VIEW

    def __repr__(self) -> str:
        return f"<MiddlewareResult action={self.action!r} target={self.target!r}>"
