"""Standalone example demonstrating TranslationManager usage.

This script lives in the `examples/` folder and points to the sample
`translations.csv` that lives in the same directory. Set flet_config
before importing the manager so that the instance picks it up.
"""

import os
import sys

# Allow running from the project root without pip install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flet_base.config import flet_config

# Point to the CSV bundled with examples
flet_config.translations_csv_path = os.path.join(os.path.dirname(__file__), "translations.csv")
flet_config.translations_csv_separator = ","
flet_config.default_language = "en"

# Import AFTER config is set so the module-level instance picks it up
from flet_base.translations.translations import TranslationManager

# Create a fresh instance (the module-level one was created before we set config)
tm = TranslationManager()


def main():
    print("Using translation CSV:", tm.csv_path)
    print("Available language codes:", tm.available_languages)
    print("Available language names:", tm.get_available_languages())
    print("Current active language:", tm.active_lang)

    # Change language synchronously (set_language with no page just updates the state)
    tm.active_lang = "es"
    print("Changed active language to", tm.active_lang)

    # Interactive key lookup
    while True:
        key = input("Enter translation key (or 'quit'): ")
        if key.lower() == "quit":
            break
        print(f"  [{tm.active_lang}] -> {tm.translate(key)}")

    # Helper functions
    print("get_language_name('fr') ->", tm.get_language_name("fr"))
    print("get_language_code('Español') ->", tm.get_language_code("Español"))
    print("Example complete.")


if __name__ == "__main__":
    main()
