"""
FletRouter: the heart of the routing system for Flet.

Features:
- Page registration with decorators (@app.page)
- Dynamic routes (/user/:id)
- Global and per-page middleware
- Shell components (AppBar, Drawer, MenuBar) applied by route
- Data sharing between pages (data.shared)
- Navigation history (data.go_back())
- Customizable 404 page
- Async support
"""

from __future__ import annotations

import inspect
from typing import Any, Callable

import flet as ft
from flet_base.config import flet_config

from .data import DataSystem
from .middleware import MiddlewareResult
from .page import PageSystem
from .shell import ShellComponent
from .utils import parse_route


class FletRouter:
    """
    Main router for Flet applications.

    Args:
        route_init: Initial route when opening the app (default: "/")
        route_login: Login route (used by route protection)
        on_error: Function called on unhandled errors
    """

    def __init__(
        self,
        route_init: str = "/",
        route_login: str = "/login",
        on_error: Callable | None = None,
    ):
        self.route_init = route_init
        self.route_login = route_login
        self.on_error_handler = on_error

        self.pages_list: list[PageSystem] = []
        self.global_middlewares_list: list[Callable] = []
        self.shells_list: list[ShellComponent] = []
        self.page_404_handler: Callable | None = None
        self.on_resize_handler: Callable | None = None
        self.on_keyboard_handler: Callable | None = None

    # ══════════════════════════════════════════════
    # PUBLIC DECORATORS
    # ══════════════════════════════════════════════

    def page(
        self,
        route: str,
        title: str | None = None,
        middlewares: list[Callable] | None = None,
        protected: bool = False,
    ) -> Callable:
        """
        Registers a page in the router.

        Args:
            route:       Page route. Accepts dynamic parameters: /user/:id
            title:       Browser/window title for this page
            middlewares: List of middlewares that only apply to this page
            protected:   If True, requires data.shared["authenticated"] to be True

        Example:
            @app.page("/home", title="Home")
            def home(data: fr.DataSystem) -> ft.View:
                return ft.View("/home", controls=[ft.Text("Home")])

            @app.page("/user/:id", title="Profile")
            def user_profile(data: fr.DataSystem) -> ft.View:
                user_id = data.param("id")
                ...
        """

        def decorator(func: Callable) -> Callable:
            self.pages_list.append(
                PageSystem(
                    route=route,
                    func=func,
                    title=title,
                    middlewares=middlewares or [],
                    protected=protected,
                )
            )
            return func

        return decorator

    def middleware(self, func: Callable) -> Callable:
        """
        Registers a global middleware that runs on EVERY route change.

        The middleware receives (data: Datasy) and must return MiddlewareResult.

        Example:
            @app.middleware
            def auth_check(data: fr.DataSystem) -> fr.MiddlewareResult:
                if data.page.route.startswith("/admin"):
                    if not data.shared.get("is_admin"):
                        return fr.MiddlewareResult.redirect("/login")
                return fr.MiddlewareResult.next()
        """
        self.global_middlewares_list.append(func)
        return func

    def shell(
        self,
        routes: list[str] | None = None,
        prefix: str | None = None,
        exclude: list[str] | None = None,
    ) -> Callable:
        """
        Registers a shell component that is applied around the page content.
        Use it for AppBar, NavigationDrawer, MenuBar, BottomNavBar, etc.

        Args:
            routes:  Exact list of routes where this shell applies
            prefix:  Route prefix: applies to all routes starting with this
            exclude: List of routes where it should NOT apply

        If neither routes nor prefix is specified, the shell applies to ALL routes.

        The decorated function receives (data: Datasy, view: ft.View) and must return ft.View.

        Example:
            # Global shell with AppBar
            @app.shell()
            def main_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
                view.appbar = ft.AppBar(title=ft.Text("My App"))
                return view

            # Shell only for the admin area
            @app.shell(prefix="/admin", exclude=["/admin/login"])
            def admin_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
                view.appbar = ft.AppBar(
                    title=ft.Text("Admin"),
                    bgcolor=ft.Colors.RED_700,
                    leading=ft.IconButton(
                        ft.Icons.ARROW_BACK,
                        on_click=data.go_back
                    )
                )
                return view

            # Shell with Windows-style menu (File, Edit, View...)
            @app.shell(exclude=["/login", "/splash"])
            def menubar_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
                view.controls.insert(0, ft.MenuBar(controls=[
                    ft.SubmenuButton(content=ft.Text("File"), controls=[
                        ft.MenuItemButton(content=ft.Text("New"), ...),
                        ft.MenuItemButton(content=ft.Text("Exit"), ...),
                    ]),
                ]))
                return view
        """

        def decorator(func: Callable) -> Callable:
            self.shells_list.append(
                ShellComponent(
                    func=func,
                    routes=routes,
                    prefix=prefix,
                    exclude=exclude,
                )
            )
            return func

        return decorator

    def page_404(self, func: Callable) -> Callable:
        """
        Registers the page shown when no route matches.

        Example:
            @app.page_404
            def not_found(data: fr.DataSystem) -> ft.View:
                return ft.View(
                    "/404",
                    controls=[
                        ft.Text("404 - Page not found", size=32),
                        ft.FilledButton("Go to home", on_click=data.go("/home")),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
        """
        self.page_404_handler = func
        return func

    def on_resize(self, func: Callable) -> Callable:
        """
        Registers a handler for the page's on_resize event.

        The function receives (data: Datasy, e: ft.ControlResizeEvent).

        Example:
            @app.on_resize
            def handle_resize(data: fr.DataSystem, e):
                print(f"New size: {e.width}x{e.height}")
        """
        self.on_resize_handler = func
        return func

    def on_keyboard(self, func: Callable) -> Callable:
        """
        Registers a global handler for keyboard events.

        The function receives (data: Datasy, e: ft.KeyboardEvent).

        Example:
            @app.on_keyboard
            def handle_key(data: fr.DataSystem, e: ft.KeyboardEvent):
                if e.key == "Escape":
                    data.go_back()
        """
        self.on_keyboard_handler = func
        return func

    # ══════════════════════════════════════════════
    # PROGRAMMATIC REGISTRATION (without decorators)
    # ══════════════════════════════════════════════

    def add_page(
        self,
        route: str,
        func: Callable,
        title: str | None = None,
        middlewares: list[Callable] | None = None,
        protected: bool = False,
    ) -> None:
        """
        Adds a page without using decorators.

        Useful for registering pages from external modules.

        Example:
            from views.home import home_view
            app.add_page("/home", home_view, title="Home")
        """
        self.pages_list.append(
            PageSystem(
                route=route,
                func=func,
                title=title,
                middlewares=middlewares or [],
                protected=protected,
            )
        )

    def add_pages(self, pages: list[dict]) -> None:
        """
        Registers multiple pages at once from a list of dicts.

        Example:
            app.add_pages([
                {"route": "/home",     "func": home_view,     "title": "Home"},
                {"route": "/settings", "func": settings_view, "title": "Settings"},
                {"route": "/user/:id", "func": user_view},
            ])
        """
        for p in pages:
            self.add_page(**p)

    # ══════════════════════════════════════════════
    # INTERNAL LOGIC
    # ══════════════════════════════════════════════

    def find_page(self, path: str) -> tuple[PageSystem | None, dict[str, str]]:
        """Searches for the page that matches the path. Static routes first."""
        # 1. Search for exact match (static routes have priority)
        for page in self.pages_list:
            if not page.is_dynamic and page.route == path:
                return page, {}

        # 2. Search for dynamic match
        for page in self.pages_list:
            if page.is_dynamic:
                params = page.match(path)
                if params is not None:
                    return page, params

        return None, {}

    async def run_middlewares(
        self,
        middlewares: list[Callable],
        data: DataSystem,
    ) -> MiddlewareResult:
        """Runs a chain of middlewares. Stops at the first one that is not .next()"""
        for mw in middlewares:
            if inspect.iscoroutinefunction(mw):
                result = await mw(data)
            else:
                result = mw(data)

            if not isinstance(result, MiddlewareResult):
                raise TypeError(
                    f"The middleware {mw.__name__!r} must return MiddlewareResult, "
                    f"not {type(result).__name__!r}. "
                    f"Use MiddlewareResult.next() to continue."
                )

            if not result.should_continue:
                return result

        return MiddlewareResult.next()

    async def apply_shells(self, path: str, data: DataSystem, view: ft.View) -> ft.View:
        """Applies all shells that correspond to the current route."""
        for shell in self.shells_list:
            if shell.applies_to(path):
                if inspect.iscoroutinefunction(shell.func):
                    view = await shell.apply(data, view)
                else:
                    view = shell.apply(data, view)
        return view

    async def build_view(self, page: PageSystem, data: DataSystem) -> ft.View | None:
        """Builds the view by calling the page function."""
        if inspect.iscoroutinefunction(page.func):
            view = await page.build(data)
        else:
            view = page.build(data)
        return view

    def handle_route_change(self, page: ft.Page) -> Callable:
        """Returns the handler for the route change event."""

        async def _handler(e: ft.RouteChangeEvent) -> None:
            full_route: str = e.route
            path, query_params = parse_route(full_route)

            # Update history (avoid duplicates on refresh)
            if not hasattr(page, "_fr_history"):
                page._fr_history = []  # type: ignore[attr-defined]
            history: list[str] = page._fr_history  # type: ignore[attr-defined]
            if not history or history[-1] != full_route:
                history.append(full_route)

            # Create base DataSystem object (no route params yet)
            data = DataSystem(page, self, query_params=query_params)

            # Run global middlewares
            global_result = await self.run_middlewares(self.global_middlewares_list, data)
            if global_result.should_redirect:
                page.push_route(global_result.target)
                return
            if global_result.has_view:
                page.views.clear()
                page.views.append(global_result.target)
                page.update()
                return

            # Find the page
            matched_page, route_params = self.find_page(path)

            if matched_page is None:
                # 404
                if self.page_404_handler:
                    if inspect.iscoroutinefunction(self.page_404_handler):
                        view_404 = await self.page_404_handler(data)
                    else:
                        view_404 = self.page_404_handler(data)
                    page.views.clear()
                    page.views.append(view_404)
                else:
                    page.views.clear()
                    page.views.append(
                        ft.View(
                            route=path,
                            controls=[
                                ft.Column(
                                    [
                                        ft.Text(
                                            "404",
                                            size=64,
                                            weight=ft.FontWeight.BOLD,
                                            font_family=flet_config.main_font_family,
                                        ),
                                        ft.Text(
                                            f"Route not found: {path}",
                                            font_family=flet_config.main_font_family,
                                        ),
                                        ft.FilledButton(
                                            content=ft.Text(
                                                "Back to start",
                                                font_family=flet_config.main_font_family,
                                            ),
                                            on_click=lambda _: page.push_route(self.route_init),
                                        ),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                )
                            ],
                            vertical_alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
                page.update()
                return

            # Complete DataSystem with route_params
            data = DataSystem(page, self, route_params=route_params, query_params=query_params)

            # Route protection
            if matched_page.protected and not data.shared.get("authenticated"):
                page.push_route(self.route_login)
                return

            # Specific page middlewares
            if matched_page.middlewares:
                page_result = await self.run_middlewares(matched_page.middlewares, data)
                if page_result.should_redirect:
                    page.push_route(page_result.target)
                    return
                if page_result.has_view:
                    page.views.clear()
                    page.views.append(page_result.target)
                    page.update()
                    return

            # Build the view
            view = await self.build_view(matched_page, data)

            if view is None:
                return

            # Apply title
            if matched_page.title:
                page.title = matched_page.title

            # Apply shells
            view = await self.apply_shells(path, data, view)

            # Update views in the stack
            page.views.clear()
            page.views.append(view)
            page.update()

        return _handler

    def handle_view_pop(self, page: ft.Page) -> Callable:
        """Handler for the system's back button."""

        def _handler(e: ft.ViewPopEvent) -> None:
            # We don't use page.views.pop() because we manage the navigation manually
            # we just call data.go_back()
            data = DataSystem(page, self)
            data.go_back()

        return _handler

    # ══════════════════════════════════════════════
    # EXECUTION
    # ══════════════════════════════════════════════

    async def main_entry(self, page: ft.Page) -> None:
        """Main entry point for the Flet application."""
        # Initialize page-specific context
        if not hasattr(page, "_fr_shared"):
            page._fr_shared = {}   # type: ignore[attr-defined]
        if not hasattr(page, "_fr_history"):
            page._fr_history = []  # type: ignore[attr-defined]

        # Register event handlers
        page.on_route_change = self.handle_route_change(page)
        page.on_view_pop = self.handle_view_pop(page)

        if self.on_resize_handler:
            def _resize_handler(e: Any) -> None:
                data = DataSystem(page, self)
                self.on_resize_handler(data, e)  # type: ignore[misc]
            page.on_resize = _resize_handler

        if self.on_keyboard_handler:
            def _keyboard_handler(e: ft.KeyboardEvent) -> None:
                data = DataSystem(page, self)
                self.on_keyboard_handler(data, e)  # type: ignore[misc]
            page.on_keyboard_event = _keyboard_handler

        if self.on_error_handler:
            def _error_handler(e: Any) -> None:
                data = DataSystem(page, self)
                self.on_error_handler(data, e)  # type: ignore[misc]
            page.on_error = _error_handler

        # Navigate to the initial route
        await page.push_route(self.route_init)

    def run(
        self,
        *,
        view: ft.AppView = ft.AppView.FLET_APP,
        assets_dir: str | None = None,
        upload_dir: str | None = None,
        web_renderer: ft.WebRenderer = ft.WebRenderer.AUTO,
        route_url_strategy: ft.RouteUrlStrategy = ft.RouteUrlStrategy.PATH,
        **kwargs: Any,
    ) -> None:
        """
        Starts the Flet application.

        Args:
            view:               View mode (desktop, web, mobile)
            assets_dir:         Directory for static assets
            upload_dir:         Directory for file uploads
            web_renderer:       Renderer for web (auto / canvaskit / html)
            route_url_strategy: URL strategy for web (path or hash)
            **kwargs:           Additional arguments for ft.run()

        Example:
            app.run()                              # Desktop
            app.run(view=ft.AppView.WEB_BROWSER)  # Web
        """
        ft.run(
            self.main_entry,
            view=view,
            assets_dir=assets_dir,
            upload_dir=upload_dir,
            web_renderer=web_renderer,
            route_url_strategy=route_url_strategy,
            **kwargs,
        )

    def get_flet_target(self) -> Callable:
        """
        Returns the target function to use with ft.app() manually.
        Useful for integrating with FastAPI or other servers.

        Example:
            import flet as ft
            import flet_fastapi
            from my_app import app as router

            flet_app = flet_fastapi.app(router.get_flet_target())
        """
        return self.main_entry

    def __repr__(self) -> str:
        return (
            f"<FletRouter pages={len(self.pages_list)} "
            f"middlewares={len(self.global_middlewares_list)} "
            f"shells={len(self.shells_list)}>"
        )
