from .router import FletRouter
from .data import DataSystem
from .middleware import MiddlewareResult
from .shell import ShellComponent
from .page import PageSystem

__all__ = [
    # ── Main classes ────────────────────────────────────────────────────────
    "FletRouter",        # Main router: creates the app and registers pages/shells/middleware
    "DataSystem",        # Object received by each page: navigation, data, parameters
    "MiddlewareResult",  # Middleware result: .next() .redirect() .view()

    # ── Support classes (useful for type hints) ─────────────────────────────
    "ShellComponent",    # Registered shell; useful for type hints in external functions
    "PageSystem",        # Registered page; useful for inspection or router extension
]
