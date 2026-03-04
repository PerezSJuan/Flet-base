# Flet-base



## Translation manager


 ## Function-by-function usage

 **`TranslationManager.__init__(csv_path=None, default_lang="en")`**
 - Creates a manager instance and immediately loads the CSV at
   `csv_path` (or `translations.csv` next to this file).
 - `default_lang` is the fallback language code when a translation
   is missing.  If you want to use a CSV from another location, simply
   pass the full path:

     tm = TranslationManager(csv_path="/path/to/my.csv")

   For example, to keep translations in a sibling `data/` folder:

     tm = TranslationManager(csv_path=os.path.join(os.getcwd(),
                                                    "data",
                                                    "translations.csv"))

   After initialization the `self.csv_path` attribute holds the actual
   file location used.

 **`get_language_name(code)` / `get_language_code(name)`**
 - These are simple helpers that map ISO codes and human-readable
   names.  They work independently of any instance and can be called
   at module level.
 - They fall back to the input if the lookup fails.

 **`awake(page)`**
 - Intended for use with a `flet.Page` object.  It reads the saved
   language from `page.shared_preferences`, or uses the page locale
   if nothing is stored.  Changes the active language accordingly and
   updates the preference.

 **`_load_csv()`** (private)
 - Reads the CSV file and populates `self.translations` and
   `self.available_languages`.  You normally won't call this
   directly; it is invoked from `__init__`.

 **`set_language(lang)`**
 - Switch the active language code used by `translate()`.
   Example: `tm.set_language("es")`.

 **`get_available_languages()`**
 - Returns a list of translated language names that appear in the
   CSV header, e.g. `['English', 'Español', 'Français']`.

 **`translate(key)`**
 - Look up a key and return the string in the current active language.
   Falls back to the default language or returns the key if nothing is
   found.  This is the method you'll use in UI code.

 ------------------------------------------------------------
 ## Example / small self-test script

 The block in examples is a small self-test script that you can run to see how it works.
