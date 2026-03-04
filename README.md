# 🚀 Flet-base Template

A premium starter kit for building multi-platform applications with Python and Flet.

---

# 🌍 Translation Manager

A robust and simple utility to manage multi-language support in **Flet** applications. This manager handles CSV-based translations, automatic language detection, and user preference persistence.

## 🚀 Key Features

*   **CSV-Powered**: Manage all your strings in a single, easy-to-edit CSV file.
*   **Auto-Detection**: Automatically initializes with the user's system language (`page.locale`).
*   **Persistence**: Integrates with `page.shared_preferences` to remember the user's language choice.
*   **Safe Failover**: Provides recursive fallback (Current Language → Default Language → Key Name).
*   **Bidirectional Mapping**: Supports converting between ISO codes (e.g., `en`) and human-readable names (e.g., `English`).

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

| key | en | es | fr | ... |
| :--- | :--- | :--- | :--- | :--- |
| hello | Hello | Hola | Bonjour | ... |
| login_btn | Login | Iniciar Sesión | Connexion | ... |

> [!TIP]
> Use standard ISO 639-1 codes (2 letters) for column headers to ensure compatibility with `page.locale`.

---

## 💡 Implementation Example

```python
import flet as ft
from translations.translations import TranslationManager

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
