"""Standalone example demonstrating TranslationManager usage.

This script lives in the `examples/` folder and imports the manager from
`translations` package.  It does **not** attempt to create a CSV next to the
example; instead it relies on the default CSV bundled with the package.  If
you want to exercise a custom file you may pass its path to the manager.
"""

import asyncio

from translations import instance_translation_manager as tm


async def main():
    # print path that will be used by the manager (default package CSV)
    print("Using translation CSV:", tm.csv_path)

    print("Available language codes:", tm.available_languages)
    print("Available language names:", tm.get_available_languages())

    print("Current active language:", tm.active_lang)
    await tm.set_language("es")
    print("Changed active language to", tm.active_lang)

    # interactive key lookup
    while True:
        key = input("Enter translation key (or 'quit'): ")
        if key.lower() == "quit":
            break
        print(f"[{tm.active_lang}] -> {tm.translate(key)}")

    # helper functions
    print("get_language_name('fr') ->", tm.get_language_name("fr"))
    print("get_language_code('Español') ->", tm.get_language_code("Español"))

    print("Example complete.")


if __name__ == "__main__":
    asyncio.run(main())
