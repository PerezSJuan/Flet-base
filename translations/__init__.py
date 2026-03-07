"""Top-level package for translations utilities.

This package exposes the :class:`TranslationManager` class along with helper
functions for dealing with language codes and names.  It is designed to be a
simple drop‑in for Flet applications that require internationalization.
"""

from .translations import (
    TranslationManager,
    LANGUAGE_NAMES,
    instance_translation_manager
)

__all__ = [
    "TranslationManager",
    "LANGUAGE_NAMES",
    "instance_translation_manager"
]
