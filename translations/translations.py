import csv
import os
from typing import Dict, List


# Mapping of language codes to their full names
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "ru": "Русский",
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
    "ar": "العربية",
    "nl": "Nederlands",
    "pl": "Polski",
    "tr": "Türkçe",
    "sv": "Svenska",
    "no": "Norsk",
    "da": "Dansk",
    "fi": "Suomi",
    "cs": "Čeština",
    "hu": "Magyar",
    "ro": "Română",
    "th": "ไทย",
    "vi": "Tiếng Việt",
    "id": "Bahasa Indonesia",
    "el": "Ελληνικά",
    "he": "עברית",
    "hi": "हिन्दी",
}


class TranslationManager:
    """Manages loading and retrieving translations from a CSV file.
    
    The CSV should have a header where the first column is the translation key
    and the subsequent columns are language codes (e.g., 'en', 'es').
    """

    def __init__(self, csv_path: str = None, default_lang: str = "en") -> None:
        if csv_path is None:
            # Default to translations.csv in the same directory as this file
            csv_path = os.path.join(os.path.dirname(__file__), "translations.csv")
            # If not found, return error
            if not os.path.isfile(csv_path):
                raise FileNotFoundError(f"Translation CSV not found at {csv_path}")

        self.csv_path = csv_path
        self.default_lang = default_lang
        self.active_lang = default_lang
        self.translations: Dict[str, Dict[str, str]] = {}
        self.available_languages: List[str] = []
        self._load_csv()

    @staticmethod
    def get_language_name(code: str) -> str:
        """Returns the full name of a language given its code.
        Falls back to the code itself if not found.
        """
        return LANGUAGE_NAMES.get(code.lower(), code)


    @staticmethod
    def get_language_code(name: str) -> str:
        """Returns the code of a language given its name.
        Falls back to the name itself if not found.
        """
        # Buscamos en los valores del diccionario ignorando mayúsculas/minúsculas
        name_lower = name.lower().strip()
        for code, lang_name in LANGUAGE_NAMES.items():
            if lang_name.lower() == name_lower:
                return code
        return name

    def awake(self, page=None) -> None:
        """
        Initialize user language preferences.
        To use this in a Flet app, create an instance and call it after
        initializing the page:

        def main(page: ft.Page):
            tm = TranslationManager()
            tm.awake(page)
            # ... rest of the app
        """
        stored_language = page.shared_preferences.get("language")
        if stored_language:
            # Ensure we have a language code (in case the full name was saved)
            self.set_language(self.get_language_code(stored_language))
        else:
            default_language = page.locale
            if default_language in self.available_languages:
                self.set_language(default_language)
            else:
                self.set_language(self.default_lang)
            page.shared_preferences.set("language", self.active_lang)

    def _load_csv(self) -> None:
        if not os.path.isfile(self.csv_path):
            return

        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                # First column is 'key', rest are languages
                self.available_languages = reader.fieldnames[1:]
                key_field = reader.fieldnames[0]
                for row in reader:
                    key = row.pop(key_field)
                    if key:
                        # Remove empty columns
                        self.translations[key] = {
                            lang: txt for lang, txt in row.items() if txt
                        }

    def set_language(self, lang: str) -> None:
        """Change the active language."""
        self.active_lang = lang

    def get_available_languages(self) -> List[str]:
        """Return a list of language names available in the CSV."""
        return [self.get_language_name(lang) for lang in self.available_languages]

    def translate(self, key: str) -> str:
        """Return the translation for key in the active language.
        Falls back to default language then the key itself.
        """
        entry = self.translations.get(key, {})
        return entry.get(self.active_lang) or entry.get(self.default_lang) or key
    
    
    
