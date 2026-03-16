"""
Utilities for parsing Flet URLs:
  /home              → path="/home", query={}
  /user/42?tab=info  → path="/user/42", query={"tab": "info"}
"""

from __future__ import annotations
from urllib.parse import urlparse, parse_qs


def parse_route(full_route: str) -> tuple[str, dict[str, str]]:
    """
    Separates the path from the query string in a Flet route.

    Returns:
        (path, query_params)
        Example: parse_route("/user/42?tab=info&debug=1")
            → ("/user/42", {"tab": "info", "debug": "1"})
    """
    parsed = urlparse(full_route)
    path = parsed.path or "/"

    # parse_qs returns lists; we take only the first value
    raw_query = parse_qs(parsed.query)
    query_params = {k: v[0] for k, v in raw_query.items()}

    return path, query_params
