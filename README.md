# 🚀 Flet-base Template

A premium starter kit for building multi-platform applications with Python and Flet.

---

## 🛠️ Initializing a New Project

This repository serves as a **template** for new Flet-based apps.  You can
start from scratch using Flet's own project generator and then layer in the
custom modules that live here.

1. **Create the base application**
   
   ```bash
   flet create my_app
   cd my_app
   ```
   
   This will generate a minimal Flet project structure (including an
   `app.py` or similar entry point) and install the core `flet` package.

2. **Install local utility modules**
   
   * `components`
   
   * `layout`
   
   * `router`
   
   * `themes`
   
   * `translations`

Some modules depends to each other, so it is recomended to install all of them even if you do not use it. 

---

# 🌍 Translation Manager

A robust and simple utility to manage multi-language support in **Flet** applications. This manager handles CSV-based translations, automatic language detection, and user preference persistence.

## 🚀 Key Features

* **CSV-Powered**: Manage all your strings in a single, easy-to-edit CSV file.
* **Auto-Detection**: Automatically initializes with the user's system language (`page.locale`).
* **Persistence**: Integrates with `page.shared_preferences` to remember the user's language choice.
* **Safe Failover**: Provides recursive fallback (Current Language → Default Language → Key Name).
* **Bidirectional Mapping**: Supports converting between ISO codes (e.g., `en`) and human-readable names (e.g., `English`).

---

## 🛠️ Internal Structure & API

### **Core Methods**

#### **`TranslationManager(csv_path=None, default_lang="en")`**

Creates a new manager instance.

- **`csv_path`**: Optional. Path to your translation file. Defaults to `translations.csv` in the same directory as the module.
- **`default_lang`**: The fallback language code.

#### **`awake(page: ft.Page)`**

The essential initialization hook for Flet apps.

1. Checks `page.shared_preferences` for a saved language.
2. If not found, attempts to use `page.locale`.
3. Falls back to `default_lang` if neither is available.

#### **`translate(key: str) -> str`**

The main method for UI strings. 

- Usage: `tm.translate("welcome_message")`

#### **`set_language(lang_code: str)`**

Updates the active language. Note: This changes the internal state; you should also update `page.shared_preferences` to persist the change.

### **Utility Helpers**

- **`get_available_languages()`**: Returns a list of readable names (e.g., `["English", "Español"]`).
- **`get_language_name(code)`**: Static method. `en` -> `English`.
- **`get_language_code(name)`**: Static method. `Español` -> `es`.

---

## 📊 CSV Format Requirement

Your `translations.csv` must follow this header structure:

| key       | en    | es             | fr        | ... |
|:--------- |:----- |:-------------- |:--------- |:--- |
| hello     | Hello | Hola           | Bonjour   | ... |
| login_btn | Login | Iniciar Sesión | Connexion | ... |

> [!TIP]
> Use standard ISO 639-1 codes (2 letters) for column headers to ensure compatibility with `page.locale`.

---

## 💡 Implementation Example

```python
import flet as ft

import os
import sys
import asyncio
root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")
if root not in sis.path:
    sys.path.insert(0,root)
from translations import instance_translation_manager as tm


async def main(page: ft.Page):
    # 1. Initialize & Awake
    await tm.awake(page)

    # 2. Reactive UI Component
    user_greeting = ft.Text(tm.translate("hello"), size=30, weight="bold")

    async def change_lang(code):
        await tm.set_language(code)
        page.shared_preferences.set("language", code)
        # Update the UI
        user_greeting.value = tm.translate("hello")
        page.update()

    page.add(
        user_greeting,
        ft.ElevatedButton(
            "Change to Spanish", 
            on_click=lambda _: await change_lang("es")
        )
    )

ft.app(target=main)
```

---

## 🧪 Testing

The `translations.py` file includes a built-in test block. You can run it directly to verify your CSV loading:

```bash
python translations/translations.py
```

---

## 🎨 Theme Manager

A lightweight helper for toggling between light and dark palettes in
Flet applications. Themes are stored in `page.shared_preferences` so that
user choices survive app restarts. The API mirrors the translation
manager for consistency.

### 🛠️ Key Features

* **Light & Dark palettes** with sensible defaults but easy to override.
* **Persistent preference** using `page.shared_preferences` under the key
  `"theme"`.
* **Automatic initialization** on page creation (`awake()`).
* **Convenience methods**: `set_light_theme`, `set_dark_theme`,
  `switch_theme`.

### 🛠️ Internal Structure & API

#### **`themes(default_theme=light_theme)`**

Constructor taking a starting palette (either `light_theme` or
`dark_theme`).

#### **`awake(page: ft.Page)`**

Reads stored preference and applies the corresponding palette; if none is
found it consults `ft.ThemeMode.SYSTEM` and the provided default. The order is:

- Checks `page.shared_preferences` for a saved theme.
- If not found, attempts to use system theme.
- Falls back to `default` if neither is available.

#### **`set_light_theme(page)` / `set_dark_theme(page)`**

Apply a specific palette and save the choice. They also update
`actual_theme` so your code can query the active color values.

#### **`switch_theme(page)`**

Toggle between light and dark. If the current palette is neither, it
falls back to `awake()` behaviour.

Even if you change theme, app's border might not change color because it is fixed in system configuration, for example in windows. 

### 🛠️Change theme colors

In `themes.py` there are two objects about colors: dark and light theme. You can modify it easily, there is only one limit: you can not have different color names in one palette than in other. Changing some color's name will probably break component scheme, so do it carefuly. 

```python
light_theme = {
    "primary": "#6200EE",
    "on_primary": "#FFFFFF",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#FFFFFF",
    "on_background": "#000000",
    "surface": "#FFFFFF",
    "on_surface": "#000000",
    "error": "#B00020",
    "on_error": "#FFFFFF",
    "warning": "#FFB300",
    "success": "#388E3C",
}

dark_theme = {
    "primary": "#BB86FC",
    "on_primary": "#000000",
    "secondary": "#03DAC6",
    "on_secondary": "#000000",
    "background": "#121212",
    "on_background": "#FFFFFF",
    "surface": "#1E1E1E",
    "on_surface": "#FFFFFF",
    "error": "#CF6679",
    "on_error": "#000000",
    "warning": "#FFB300",
    "success": "#66BB6A",
}
```

---

### 💡 Theme Example

```python
import os
import sys
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from themes.themes import instance_themes as themes


def main(page: ft.Page):
    th = themes()
    th.awake(page)

    txt = ft.Text("Hello, world!", size=30)

    def on_click(_):
        th.switch_theme(page)
        # update UI colors (demo uses the palette directly)
        txt.color = th.actual_theme["primary"]
        page.update()

    page.add(
        txt,
        ft.ElevatedButton("Toggle theme", on_click=on_click),
    )

ft.app(target=main)
```

---

# 🔘 Components: Buttons

The `components/buttons.py` module provides a set of pre-styled button helpers that automatically integrate with the active theme. This ensures visual consistency across your application with minimal code.

## 🚀 Key Features

* **Theme Integration**: Buttons automatically use colors from `themes.actual_theme`. **Use themes is required to use any component.**
* **Simplified API**: Quick creation of common button styles (filled, icon-only, text-only).
* **State Management**: Easy toggling of the `enabled` state.

---

## 🛠️ API Reference

### **`filled_btn(text, icon=None, on_click=None, enabled=True)`**

Creates a standard filled button using the theme's `primary` color for the background and `on_primary` for the content.

### **`icon_filled_btn(icon, on_click=None, enabled=True)`**

An icon-only version of the filled button.

### **`icon_btn(icon, on_click=None, enabled=True)`**

A transparent background button that uses the `primary` color for the icon itself.

### **`text_btn(text, icon=None, on_click=None, enabled=True)`**

A flat button without a background, useful for secondary actions or navigation links. Uses the theme's `text_color`.

### **`btn(text, icon=None, on_click=None, enabled=True, ...)`**

A more flexible filled button that allows you to specify custom light and dark mode colors manually.

---

## 🧪 Usage Example

```python
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from components.buttons import filled_btn, icon_btn, text_btn
from themes.themes import instance_themes as themes

async def main(page: ft.Page):
    await themes.awake(page)

    page.add(
        filled_btn("Submit", on_click=lambda _: print("Submit clicked!")),
        icon_btn(ft.Icons.DELETE, on_click=lambda _: print("Delete clicked!")),
        text_btn("Cancel", on_click=lambda _: page.window_close()),
    )

ft.app(target=main)
```

---

# 📝 Components: Texts

The `components/texts.py` module provides a variety of text styles and helpers that seamlessly integrate with your application's theme.

## 🚀 Key Features

* **Theme Consistency**: All text components automatically use the appropriate colors from your theme (e.g., `text_color`, `primary`, `secondary`, `error`).
* **Semantic Styling**: Pre-defined styles for titles, subtitles, body text, and captions.
* **Rich Content**: Support for Markdown and clickable links.

---

## 🛠️ API Reference

### Titles & Subtitles

* **`title(text, ...)`**: Main title style using the theme's default text color.
* **`title_primary(text, ...)`**: Title using the `primary` color.
* **`title_secondary(text, ...)`**: Title using the `secondary` color.
* **`subtitle(text, ...)`**: Standard subtitle style.
* **`subtitle_primary(text, ...)` / `subtitle_secondary(text, ...)`**: Subtitles with theme colors.

### Body & Utilities

* **`body(text, ...)`**: Standard body text.
* **`caption(text, ...)`**: Small text for descriptions or notes.
* **`error_text(text, ...)`**: Themed red text for error messages.
* **`markdown(md, ...)`**: Renders markdown content with theme-aware styling.
* **`link(url, page, text=None, ...)`**: Creates a clickable `TextButton` that opens a URL.

---

## 🧪 Usage Example

```python
import flet as ft

# ensure parent folder (workspace root) is on import path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from components.texts import title, subtitle, body, link
from themes.themes import instance_themes as themes

async def main(page: ft.Page):
    await themes.awake(page)

    page.add(
        title("Welcome to Flet-base"),
        subtitle("A premium starter kit"),
        body("This is a standard body text using the theme's colors."),
        await link("https://flet.dev", page, "Visit Flet Website")
    )

ft.app(target=main)
```

---

# 📊 Components: Data Display

The `components/data_display.py` module includes components for presenting data and media, all styled to match your theme.

## 🚀 Key Features

* **Interactive Data**: Simplified `DataTable` integration.
* **Visual Feedback**: Themed progress bars and loading indicators.
* **Media Support**: Easy icon and image helpers.
* **Layout Helpers**: Collapsible panels and themed material cards.

---

## 🛠️ API Reference

### **`datatable(columns, rows, ...)`**

A themed version of `DataTable2` with pre-configured spacing and header colors.

### **`icon(icon, color=None, size=24)`**

Creates an icon that defaults to the theme's `primary` color.

### **`image(src, width=100, height=100, border_radius=5)`**

A simple image helper with a default border radius.

### **`progress_bar(value, ...)`**

A linear progress bar styled with theme colors (`primary` for progress, `surface` for background).

### **`loading_indicator(size=50)`**

A circular progress ring (loading spinner) using the theme's `primary` color.

### **`expansion_panel(header, content=[], expanded=False)`**

A collapsible panel with a `surface`-themed background. Wrap one or more inside a `ft.ExpansionPanelList` to allow only one open at a time.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `header` | `str` | — | Label shown in the collapsed header bar. |
| `content` | `list` | `[]` | Flet controls rendered inside the expanded body. |
| `expanded` | `bool` | `False` | Whether the panel starts already open. |

### **`card(content=[], color=None)`**

A material card with padding and an optional custom background color. Defaults to the theme's `primary` color.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `list` | `[]` | Flet controls placed inside the card body. |
| `color` | `str \| None` | `None` | Card background. Falls back to `primary` if omitted. |

---

## 🧪 Usage Example

```python
import os, sys
import flet as ft

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from components.data_display import (
    icon, progress_bar, loading_indicator,
    expansion_panel, card,
)
from components.texts import body, caption
from themes.themes import instance_themes as themes

async def main(page: ft.Page):
    await themes.awake(page)

    page.add(
        # Basic display
        icon(ft.Icons.FAVORITE),
        progress_bar(value=0.7),
        loading_indicator(size=30),

        # Collapsible panel
        ft.ExpansionPanelList(
            controls=[
                expansion_panel(
                    header="Details",
                    content=[body("Panel content goes here.")],
                    expanded=True,
                ),
            ]
        ),

        # Material card
        card(
            content=[
                body("A themed card"),
                caption("Optional sub-text."),
            ]
        ),
    )

ft.app(target=main)
```
