"""Reference solution for Part C — the `read_page` tool.

web_search gives you titles and short snippets. The real details of an event —
the exact date, the venue, how to sign up — live on the event's own page. This
tool lets the agent *fetch* a page and read it, so it can go
`search -> open the best result -> pull out the details`: a genuine two-step
agent loop.

Copy `_extract_text` and `_read_page` next to `_web_search` in agent/tools.py,
add the Tool(...) to BUILTIN_TOOLS, then delete the skip line in
tests/test_part_c.py.
"""

import re
import urllib.request

from agent.tools import Tool


def _extract_text(html: str) -> str:
    """Turn a page's HTML into readable plain text (strip tags + scripts)."""
    html = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", text).strip()


def _read_page(args: dict) -> str:
    url = args.get("url", "").strip()
    if not url:
        return "read_page error: no url given"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", "ignore")
    except Exception as exc:
        return f"read_page error: {type(exc).__name__}: {exc}"
    return _extract_text(html)[:1500]


READ_PAGE_TOOL = Tool(
    name="read_page",
    description="Fetch a web page and return its readable text. Use this after "
                "web_search to open a promising result and pull out the details "
                "(exact date, venue, how to sign up).",
    input_schema={
        "type": "object",
        "properties": {"url": {"type": "string", "description": "The page URL to read"}},
        "required": ["url"],
    },
    run=_read_page,
)
