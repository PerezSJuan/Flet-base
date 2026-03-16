import csv
import os
from typing import Dict, List
import flet as ft

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

    
    def __init__(self, csv_path: str = None, default_lang: str = None) -> None:
        try:
            from flet_base.config import flet_config
            if csv_path is None:
                csv_path = flet_config.translations_csv_path
            if default_lang is None:
                default_lang = getattr(flet_config, "default_language", "en")
        except ImportError:
            pass
            
        if default_lang is None:
            default_lang = "en"
            
        self.csv_path = csv_path
        self.default_lang = default_lang
        self.active_lang = default_lang
        self.translations: Dict[str, Dict[str, str]] = {}
        self.available_languages: List[str] = [default_lang]
        
        if self.csv_path and os.path.isfile(self.csv_path):
            self._load_csv()
        elif self.csv_path:
            print(f"Warning: Translation CSV not found at {self.csv_path}. Proceeding with default empty dictionary.")

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
        name_lower = name.lower().strip()
        for code, lang_name in LANGUAGE_NAMES.items():
            if lang_name.lower() == name_lower:
                return code
        return name

    async def awake(self, page: ft.Page) -> None:
        """Initialize user language preferences from SharedPreferences().

        Call this once after the page is ready:

            async def main(page: ft.Page):
                tm = TranslationManager()
                await tm.awake(page)
        """
        self._page = page

        stored_language = await ft.SharedPreferences().get("language")
        if stored_language:
            # Ensure we have a language code (in case the full name was saved)
            self.active_lang = self.get_language_code(stored_language)
        else:
            # Try to use the system locale
            try:
                default_language = page.locale.language_code
            except Exception:
                default_language = None

            if default_language and default_language in self.available_languages:
                self.active_lang = default_language
            else:
                self.active_lang = self.default_lang

            await ft.SharedPreferences().set("language", self.active_lang)

    def _load_csv(self) -> None:
        if not os.path.isfile(self.csv_path):
            return

        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames:
                self.available_languages = list(reader.fieldnames[1:])
                key_field = reader.fieldnames[0]
                for row in reader:
                    key = row.pop(key_field)
                    if key:
                        self.translations[key] = {
                            lang: txt for lang, txt in row.items() if txt
                        }

    async def set_language(self, lang: str, page: ft.Page = None) -> None:
        """Change the active language and persist the choice."""
        self.active_lang = lang
        target_page = page or getattr(self, "_page", None)
        if target_page:
            await ft.SharedPreferences().set("language", self.active_lang)
            target_page.update()

    def get_available_languages(self) -> List[str]:
        """Return a list of language names available in the CSV."""
        return [self.get_language_name(lang) for lang in self.available_languages]

    def translate(self, key: str) -> str:
        """Return the translation for key in the active language.
        Falls back to default language then the key itself.
        """
        entry = self.translations.get(key, {})
        return entry.get(self.active_lang) or entry.get(self.default_lang) or key


instance_translation_manager = TranslationManager()
