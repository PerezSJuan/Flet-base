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
root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")
if root not in sis.path:
    sys.path.insert(0,root)
from translations import TranslationManager


def main(page: ft.Page):
    # 1. Initialize & Awake
    tm = TranslationManager()
    tm.awake(page)

    # 2. Reactive UI Component
    user_greeting = ft.Text(tm.translate("hello"), size=30, weight="bold")

    def change_lang(code):
        tm.set_language(code)
        page.shared_preferences.set("language", code)
        # Update the UI
        user_greeting.value = tm.translate("hello")
        page.update()

    page.add(
        user_greeting,
        ft.ElevatedButton(
            "Change to Spanish", 
            on_click=lambda _: change_lang("es")
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

from themes.themes import themes


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
