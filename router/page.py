"""
Pagesy: represents a page registered in the router.
"""

from __future__ import annotations
import re
from typing import Callable, Any


class PageSystem:
    """
    Contains the definition of a page: its route pattern,
    the function that builds it, title, its own middlewares, etc.
    """

    # Converts /user/:id  →  regex with named group 'id'
    PARAM_RE = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*)")

    def __init__(
        self,
        route: str,
        func: Callable,
        title: str | None = None,
        middlewares: list[Callable] | None = None,
        protected: bool = False,
    ):
        self.route = route
        self.func = func
        self.title = title
        self.middlewares: list[Callable] = middlewares or []
        self.protected = protected

        # Compile regex for dynamic routes
        self.param_names = self.PARAM_RE.findall(route)
        pattern = self.PARAM_RE.sub(r"(?P<\1>[^/]+)", re.escape(route))
        # re.escape escapes the slash, we restore it
        pattern = pattern.replace(r"\/", "/")
        self.regex = re.compile(f"^{pattern}$")

    @property
    def is_dynamic(self) -> bool:
        """Does the route have dynamic parameters? (/user/:id)"""
        return bool(self.param_names)

    def match(self, path: str) -> dict[str, str] | None:
        """
        Tries to match with the given path.
        Returns a dict with captured parameters, or None if it doesn't match.
        """
        m = self.regex.match(path)
        if m is None:
            return None
        return m.groupdict()

    def build(self, data: Any) -> Any:
        """
        Calls the page function with the DataSystem object.
        Supports sync and async functions.
        """
        return self.func(data)

    def __repr__(self) -> str:
        return f"<PageSystem route={self.route!r} dynamic={self.is_dynamic}>"
