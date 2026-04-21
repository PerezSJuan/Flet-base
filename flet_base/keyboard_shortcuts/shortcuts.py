import flet as ft
import platform
import logging
import asyncio
from typing import Callable, Dict, List

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ShortcutManager")


class ShortcutManager:
    """
    Manages keyboard shortcuts by mapping key combinations directly to actions.
    Example: manager.register("mod+s", save_function)
    """

    def __init__(self):
        # Determine primary modifier based on OS
        # "mod" -> "ctrl" on Windows/Linux, "meta" (Command) on macOS
        self.os_primary_mod = "meta" if platform.system() == "Darwin" else "ctrl"

        # Internal mapping: normalized_shortcut -> callback_function
        self.shortcuts: Dict[str, Callable] = {}

        # Modifier names to ignore when they appear as the primary key in events
        self._modifier_names = {
            "control",
            "ctrl",
            "shift",
            "alt",
            "meta",
            "command",
            "cmd",
            "windows",
            "win",
        }

    def register(self, shortcut_str: str, callback: Callable):
        """
        Directly registers a keyboard shortcut string to a callback function.
        Example: manager.register("mod+shift+p", my_action)
        """
        if not callable(callback):
            raise ValueError(f"Callback for '{shortcut_str}' must be callable.")

        normalized = self._normalize_shortcut_string(shortcut_str)
        self.shortcuts[normalized] = callback
        logger.info(f"Registered shortcut: {shortcut_str} ({normalized})")

    def register_many(self, shortcuts_dict: Dict[str, Callable]):
        """Registers multiple shortcuts from a dictionary."""
        for shortcut, cb in shortcuts_dict.items():
            self.register(shortcut, cb)

    def _normalize_shortcut_string(self, shortcut_str: str) -> str:
        """Normalizes a shortcut string (e.g., 'mod+s' -> 'ctrl+s')."""
        parts = shortcut_str.lower().split("+")
        resolved = []
        for p in parts:
            p = p.strip()
            if p in ["mod", "primary"]:
                resolved.append(self.os_primary_mod)
            elif p in ["cmd", "command"]:
                resolved.append("meta")
            elif p == "win":
                resolved.append("meta")
            else:
                resolved.append(p)
        return self._order_parts(resolved)

    def _order_parts(self, parts: List[str]) -> str:
        """Orders parts for consistent comparison."""
        priority = {"ctrl": 0, "alt": 1, "shift": 2, "meta": 3}
        modifiers = [p for p in parts if p in priority]
        keys = [p for p in parts if p not in priority]

        modifiers.sort(key=lambda x: priority[x])
        keys.sort()

        unique_parts = []
        seen = set()
        for p in modifiers + keys:
            if p and p not in seen:
                unique_parts.append(p)
                seen.add(p)
        return "+".join(unique_parts)

    def _get_event_shortcut_string(self, e: ft.KeyboardEvent) -> str:
        """Converts Flet event into a normalized string."""
        parts = []
        if e.ctrl:
            parts.append("ctrl")
        if e.alt:
            parts.append("alt")
        if e.shift:
            parts.append("shift")
        if e.meta:
            parts.append("meta")

        key = e.key.lower() if e.key else ""
        if key and key not in self._modifier_names:
            parts.append(key)
        return self._order_parts(parts)

    async def handle_event(self, e: ft.KeyboardEvent):
        """Main event handler. Executes registered callbacks."""
        shortcut_event = self._get_event_shortcut_string(e)
        if not shortcut_event:
            return

        if shortcut_event in self.shortcuts:
            callback = self.shortcuts[shortcut_event]
            logger.info(f"Executing shortcut: {shortcut_event}")
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback()
                else:
                    callback()
            except Exception as err:
                logger.error(f"Error in shortcut action '{shortcut_event}': {err}")
