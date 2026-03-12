import flet as ft
import router as fr


# ══════════════════════════════════════════════════════════════════════════════
# 1. CREATE THE ROUTER
# ══════════════════════════════════════════════════════════════════════════════

app = fr.FletRouter(
    route_init="/login",  # Initial route when opening the app
    route_login="/login",  # Redirect here if protected=True and no session
)


# ══════════════════════════════════════════════════════════════════════════════
# 2. GLOBAL MIDDLEWARE — Logging for each route change
# ══════════════════════════════════════════════════════════════════════════════


@app.middleware
def log_navigation(data: fr.DataSystem) -> fr.MiddlewareResult:
    """Executes on EVERY route change. Just logs and continues."""
    print(f"[nav] {data.page.route}  |  shared keys: {list(data.shared.keys())}")
    return fr.MiddlewareResult.next()


# ══════════════════════════════════════════════════════════════════════════════
# 3. GLOBAL MIDDLEWARE — Authentication Guard
#    Blocks /admin/* if user is not admin,
#    without needing to put middleware on every admin page.
# ══════════════════════════════════════════════════════════════════════════════


@app.middleware
def global_auth_guard(data: fr.DataSystem) -> fr.MiddlewareResult:
    route = data.page.route
    # Public routes: always let them pass
    if route in ("/login", "/404"):
        return fr.MiddlewareResult.next()
    # Admin area: requires role
    if route.startswith("/admin") and not data.shared.get("is_admin"):
        return fr.MiddlewareResult.redirect("/login")
    return fr.MiddlewareResult.next()


# ══════════════════════════════════════════════════════════════════════════════
# 4. GLOBAL SHELL — Android-style AppBar
#    Applies to all routes except /login.
#    Shows back button if not on /home.
# ══════════════════════════════════════════════════════════════════════════════


@app.shell(exclude=["/login"])
def appbar_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
    is_root = data.page.route in ("/home",)
    user = data.shared.get("user", "?")

    view.appbar = ft.AppBar(
        leading=None
        if is_root
        else ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            tooltip="Back",
            on_click=lambda _: data.go_back(),
        ),
        title=ft.Text(data.page.title or "App", color=ft.Colors.WHITE),
        bgcolor=ft.Colors.INDIGO_700,
        actions=[
            ft.Chip(
                label=ft.Text(user, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.INDIGO_500,
            ),
            ft.IconButton(
                icon=ft.Icons.LOGOUT,
                icon_color=ft.Colors.WHITE,
                tooltip="Logout",
                on_click=_logout(data),
            ),
        ],
    )
    return view


def _logout(data: fr.DataSystem):
    """Logs out by clearing shared data and redirecting to login."""

    def handler(e):
        data.shared.clear()
        data.page.go("/login")

    return handler


# ══════════════════════════════════════════════════════════════════════════════
# 5. PREFIX SHELL — Windows-style MenuBar only on /admin
#    Stacked on global AppBar: both shells apply to /admin/*.
# ══════════════════════════════════════════════════════════════════════════════


@app.shell(prefix="/admin")
def admin_menubar_shell(data: fr.DataSystem, view: ft.View) -> ft.View:
    menubar = ft.MenuBar(
        style=ft.MenuStyle(bgcolor=ft.Colors.GREY_100),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.HOME),
                        content=ft.Text("Home"),
                        on_click=data.go("/home"),
                    ),
                    ft.Divider(height=1),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.EXIT_TO_APP),
                        content=ft.Text("Exit"),
                        on_click=lambda _: data.page.window.close(),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("View"),
                controls=[
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.DASHBOARD),
                        content=ft.Text("Dashboard"),
                        on_click=data.go("/admin/dashboard"),
                    ),
                    ft.MenuItemButton(
                        leading=ft.Icon(ft.Icons.PEOPLE),
                        content=ft.Text("Users"),
                        on_click=data.go("/admin/users"),
                    ),
                ],
            ),
        ],
    )
    # Insert menubar before page content
    view.controls.insert(0, menubar)
    return view


# ══════════════════════════════════════════════════════════════════════════════
# 6. GLOBAL KEYBOARD EVENT
#    F1 → Home, Escape → go back, Ctrl+L → Login (demo)
# ══════════════════════════════════════════════════════════════════════════════


@app.on_keyboard
def handle_keyboard(data: fr.DataSystem, e: ft.KeyboardEvent) -> None:
    if e.key == "F1":
        data.page.go("/home")
    elif e.key == "Escape":
        data.go_back()
    elif e.key == "L" and e.ctrl:
        data.page.go("/login")


# ══════════════════════════════════════════════════════════════════════════════
# 7. GLOBAL RESIZE EVENT
# ══════════════════════════════════════════════════════════════════════════════


@app.on_resize
def handle_resize(data: fr.DataSystem, e) -> None:
    w = data.page.width
    h = data.page.height
    print(f"[resize] {w:.0f} × {h:.0f}")


# ══════════════════════════════════════════════════════════════════════════════
# 8. PUBLIC PAGE — Login
#    No protection. Saves data to shared and navigates to /home.
# ══════════════════════════════════════════════════════════════════════════════


@app.page("/login", title="Login")
def login_page(data: fr.DataSystem) -> ft.View:
    name_field = ft.TextField(label="User", autofocus=True, width=320)
    pass_field = ft.TextField(
        label="Password", password=True, can_reveal_password=True, width=320
    )
    error_label = ft.Text("", color=ft.Colors.RED_600)

    def do_login(e):
        u, p = name_field.value.strip(), pass_field.value
        if not u or not p:
            error_label.value = "Fill all fields"
            data.page.update()
            return
        # Demo credentials
        data.shared["authenticated"] = True
        data.shared["user"] = u
        data.shared["is_admin"] = u == "admin" and p == "admin"
        data.page.go("/home")

    return ft.View(
        route="/login",
        bgcolor=ft.Colors.INDIGO_50,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                padding=40,
                shadow=ft.BoxShadow(blur_radius=24, color=ft.Colors.INDIGO_100),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=14,
                    controls=[
                        ft.Icon(
                            ft.Icons.LOCK_OUTLINE, size=52, color=ft.Colors.INDIGO_700
                        ),
                        ft.Text("Bienvenido", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "admin / admin  →  acceso de administrador\n"
                            "cualquier otro  →  usuario normal",
                            size=11,
                            color=ft.Colors.GREY_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        name_field,
                        pass_field,
                        error_label,
                        ft.ElevatedButton(
                            "Entrar",
                            width=320,
                            on_click=do_login,
                            style=ft.ButtonStyle(bgcolor=ft.Colors.INDIGO_700),
                            color=ft.Colors.WHITE,
                        ),
                    ],
                ),
            )
        ],
    )


# ══════════════════════════════════════════════════════════════════════════════
# 9. PAGE WITH protected=True — Home
#    If no session exists, the router automatically redirects to route_login.
# ══════════════════════════════════════════════════════════════════════════════


@app.page("/home", title="Home", protected=True)
def home_page(data: fr.DataSystem) -> ft.View:
    user = data.shared.get("user", "?")
    is_admin = data.shared.get("is_admin", False)

    nav_buttons = [
        _nav_card("📋 Items", "Lista de items", data.go("/items")),
        _nav_card(
            "👤 Mi perfil", "Ver y editar tu perfil", data.go(f"/profile/{user}")
        ),
        _nav_card(
            "🔗 Ruta rara", "Prueba /ruta/que/no/existe", data.go("/esto/no/existe")
        ),
    ]
    if is_admin:
        nav_buttons.append(
            _nav_card(
                "🔒 Admin",
                "Panel de administración",
                data.go("/admin/dashboard"),
                color=ft.Colors.RED_50,
            )
        )

    return ft.View(
        route="/home",
        padding=30,
        controls=[
            ft.Text(f"Hello, {user} 👋", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("What would you like to do?", color=ft.Colors.GREY_600),
            ft.Divider(height=24),
            ft.Column(
                controls=nav_buttons,
                spacing=12,
            ),
            ft.Divider(height=24),
            _history_panel(data),
        ],
    )


# ══════════════════════════════════════════════════════════════════════════════
# 10. PAGE WITH protected + CUSTOM MIDDLEWARE — Items
#     The custom middleware checks an extra condition (demo: always passes).
# ══════════════════════════════════════════════════════════════════════════════


def check_items_access(data: fr.DataSystem) -> fr.MiddlewareResult:
    """Page middleware: could verify permissions, feature flags, etc."""
    if data.shared.get("items_banned"):
        # Shows an inline block view instead of redirecting
        return fr.MiddlewareResult.view(
            ft.View(
                route="/items",
                controls=[
                    ft.Column(
                        [
                            ft.Icon(ft.Icons.BLOCK, size=60, color=ft.Colors.RED),
                            ft.Text("Access to items blocked.", size=20),
                            ft.ElevatedButton("Back", on_click=data.go("/home")),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    return fr.MiddlewareResult.next()


ITEMS = [
    {"id": "1", "name": "Teclado mecánico", "price": 89},
    {"id": "2", "name": "Monitor 4K", "price": 399},
    {"id": "3", "name": "Ratón inalámbrico", "price": 45},
    {"id": "4", "name": "Auriculares HiFi", "price": 149},
]


@app.page("/items", title="Items", protected=True, middlewares=[check_items_access])
def items_page(data: fr.DataSystem) -> ft.View:
    return ft.View(
        route="/items",
        padding=24,
        controls=[
            ft.Text("Available Items", size=24, weight=ft.FontWeight.BOLD),
            ft.ListView(
                expand=True,
                spacing=8,
                controls=[
                    ft.ListTile(
                        leading=ft.CircleAvatar(
                            content=ft.Text(item["name"][0]),
                            bgcolor=ft.Colors.INDIGO_100,
                        ),
                        title=ft.Text(item["name"]),
                        subtitle=ft.Text(f"${item['price']}"),
                        trailing=ft.IconButton(
                            ft.Icons.ARROW_FORWARD_IOS,
                            on_click=data.go(f"/item/{item['id']}"),
                        ),
                    )
                    for item in ITEMS
                ],
            ),
        ],
    )


# ══════════════════════════════════════════════════════════════════════════════
# 11. DYNAMIC ROUTE + QUERY STRING — /item/:id?mode=view|edit
#     data.param("id")    → segment of the URL
#     data.query("mode")  → parameter from the query string
# ══════════════════════════════════════════════════════════════════════════════


@app.page("/item/:id", title="Detalle de item", protected=True)
def item_detail(data: fr.DataSystem) -> ft.View:
    item_id = data.param("id")  # /item/42  → "42"
    mode = data.query("mode", "view")  # ?mode=edit → "edit"

    item = next((i for i in ITEMS if i["id"] == item_id), None)
    if item is None:
        return ft.View(
            route="/item/404",
            controls=[
                ft.Text(f"Item '{item_id}' not found."),
                ft.ElevatedButton("← Items", on_click=data.go("/items")),
            ],
        )

    name_field = ft.TextField(
        value=item["name"], label="Name", disabled=(mode != "edit")
    )
    price_field = ft.TextField(
        value=str(item["price"]), label="Price", disabled=(mode != "edit")
    )

    controls = [
        ft.Text(f"Item #{item_id}", size=22, weight=ft.FontWeight.BOLD),
        ft.Text(
            f"Mode: {'✏️ edit' if mode == 'edit' else '👁 view'}",
            color=ft.Colors.GREY_600,
        ),
        name_field,
        price_field,
        ft.Row(
            [
                ft.ElevatedButton(
                    "Edit" if mode == "view" else "View",
                    on_click=data.go(
                        f"/item/{item_id}",
                        # go() accepts kwargs that are passed to data.shared
                        # but here we use query string in the URL directly:
                    )
                    if mode == "edit"
                    else lambda _: data.page.go(f"/item/{item_id}?mode=edit"),
                ),
                ft.OutlinedButton("← Items", on_click=data.go("/items")),
            ],
            spacing=12,
        ),
    ]

    return ft.View(
        route="/item/:id", padding=24, controls=[ft.Column(controls, spacing=16)]
    )


# ══════════════════════════════════════════════════════════════════════════════
# 12. DYNAMIC ROUTE — /profile/:username
#     Demonstrates data.param() and data.go() with extra parameters in shared.
# ══════════════════════════════════════════════════════════════════════════════


@app.page("/profile/:username", title="Perfil", protected=True)
def profile_page(data: fr.DataSystem) -> ft.View:
    username = data.param("username")
    own = username == data.shared.get("user")

    return ft.View(
        route=f"/profile/{username}",
        padding=24,
        controls=[
            ft.Column(
                [
                    ft.CircleAvatar(
                        content=ft.Text(username[0].upper(), size=28),
                        bgcolor=ft.Colors.INDIGO_200,
                        radius=44,
                    ),
                    ft.Text(f"@{username}", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "(This is your profile)" if own else "(Other user's profile)",
                        color=ft.Colors.GREY_500,
                    ),
                    ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.EMAIL),
                        title=ft.Text(f"{username}@ejemplo.com"),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CALENDAR_TODAY),
                        title=ft.Text("Member since 2024"),
                    ),
                    ft.ElevatedButton("← Back", on_click=lambda _: data.go_back()),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        ],
    )


# ══════════════════════════════════════════════════════════════════════════════
# 13. PROGRAMMATIC REGISTRATION — app.add_pages([...])
#     Demonstrates that not everything has to be a decorator.
#     These /admin pages are defined as normal functions
#     and registered all at once at the end.
# ══════════════════════════════════════════════════════════════════════════════


def admin_dashboard(data: fr.DataSystem) -> ft.View:
    return ft.View(
        route="/admin/dashboard",
        padding=24,
        controls=[
            ft.Column(
                [
                    ft.Text("Admin Dashboard", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            _stat_card(
                                "Users", "1,234", ft.Icons.PEOPLE, ft.Colors.BLUE
                            ),
                            _stat_card(
                                "Items", "42", ft.Icons.INVENTORY, ft.Colors.GREEN
                            ),
                            _stat_card(
                                "Alerts", "3", ft.Icons.WARNING, ft.Colors.ORANGE
                            ),
                            _stat_card("Errors", "0", ft.Icons.ERROR, ft.Colors.RED),
                        ],
                        wrap=True,
                        spacing=12,
                    ),
                    ft.Divider(),
                    ft.ElevatedButton("View users", on_click=data.go("/admin/users")),
                    ft.OutlinedButton("← Home", on_click=data.go("/home")),
                ],
                spacing=16,
            ),
        ],
    )


def admin_users(data: fr.DataSystem) -> ft.View:
    users = [
        {"name": "admin", "role": "Administrator", "active": True},
        {"name": "alice", "role": "Editor", "active": True},
        {"name": "bob", "role": "Reader", "active": False},
    ]
    return ft.View(
        route="/admin/users",
        padding=24,
        controls=[
            ft.Text("User Management", size=22, weight=ft.FontWeight.BOLD),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("User")),
                    ft.DataColumn(ft.Text("Role")),
                    ft.DataColumn(ft.Text("Active")),
                    ft.DataColumn(ft.Text("")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(u["name"])),
                            ft.DataCell(ft.Text(u["role"])),
                            ft.DataCell(
                                ft.Icon(
                                    ft.Icons.CHECK_CIRCLE
                                    if u["active"]
                                    else ft.Icons.CANCEL,
                                    color=ft.Colors.GREEN
                                    if u["active"]
                                    else ft.Colors.RED,
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    ft.Icons.PERSON,
                                    on_click=data.go(f"/profile/{u['name']}"),
                                )
                            ),
                        ]
                    )
                    for u in users
                ],
            ),
        ],
    )


# Programmatic registration of admin pages
app.add_pages(
    [
        {
            "route": "/admin/dashboard",
            "func": admin_dashboard,
            "title": "Admin: Dashboard",
        },
        {"route": "/admin/users", "func": admin_users, "title": "Admin: Users"},
    ]
)


# ══════════════════════════════════════════════════════════════════════════════
# 14. CUSTOM 404 PAGE
# ══════════════════════════════════════════════════════════════════════════════


@app.page_404
def not_found(data: fr.DataSystem) -> ft.View:
    bad_route = data.page.route
    return ft.View(
        route="/404",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text(
                        "404",
                        size=80,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.INDIGO_200,
                    ),
                    ft.Text("Page not found", size=22),
                    ft.Text(f"'{bad_route}' does not exist.", color=ft.Colors.GREY_500),
                    ft.Divider(height=20),
                    ft.ElevatedButton("← Home", on_click=data.go("/home")),
                    ft.OutlinedButton("← Back", on_click=lambda _: data.go_back()),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
        ],
    )


# ══════════════════════════════════════════════════════════════════════════════
# UI HELPERS (not part of the router, just visual utilities)
# ══════════════════════════════════════════════════════════════════════════════


def _nav_card(title: str, subtitle: str, on_click, color=ft.Colors.INDIGO_50):
    return ft.Container(
        bgcolor=color,
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=20, vertical=14),
        ink=True,
        on_click=on_click,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(title, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitle, size=12, color=ft.Colors.GREY_600),
                    ],
                    expand=True,
                    spacing=2,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400),
            ]
        ),
    )


def _stat_card(label: str, value: str, icon: str, color: str):
    return ft.Container(
        width=130,
        height=110,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.GREY_200),
        padding=12,
        content=ft.Column(
            [
                ft.Icon(icon, color=color, size=28),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                ft.Text(label, size=11, color=ft.Colors.GREY_600),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        ),
    )


def _history_panel(data: fr.DataSystem) -> ft.Control:
    """Shows the history of visited routes (demonstrates data.history)."""
    history = data.history[-8:]  # last 8
    return ft.Container(
        bgcolor=ft.Colors.GREY_50,
        border_radius=10,
        padding=14,
        content=ft.Column(
            [
                ft.Text(
                    "Navigation History",
                    weight=ft.FontWeight.W_600,
                    color=ft.Colors.GREY_700,
                ),
                ft.Text(
                    " → ".join(history) if history else "(empty)",
                    size=11,
                    color=ft.Colors.GREY_500,
                ),
            ],
            spacing=4,
        ),
    )


# ══════════════════════════════════════════════════════════════════════════════
# START
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{app}")
    print(f"Pages:       {[p.route for p in app.pages_list]}")
    print(f"Middlewares: {[m.__name__ for m in app.global_middlewares_list]}")
    print(f"Shells:      {app.shells_list}\n")

    app.run()
