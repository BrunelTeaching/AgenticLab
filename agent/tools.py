"""Component: TOOLS — the actions the agent can take.

From the lecture: *a tool is a name, a description and an input schema.* The
model reads the name + description to decide whether to call it, and fills in
arguments that match the schema. The harness then runs the tool and feeds the
result back to the model.

This agent ships with one tool: `web_search`. The model has no live knowledge
of today's world, so when a question needs current or specific facts it can
*choose* to search — that choice, made by the model and carried out by this
code, is the agent loop in miniature.

In Part C you add a second tool and watch the model pick between them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class Tool:
    name: str
    description: str
    input_schema: dict
    run: Callable[[dict], str]

    def schema(self) -> dict:
        """The shape the model needs: an OpenAI 'function' tool definition."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema,
            },
        }


def _web_search(args: dict) -> str:
    """Search the web (DuckDuckGo) and return the top results as text.

    DuckDuckGo throttles rapid calls and sometimes returns nothing transiently,
    so we retry a couple of times with a short pause before giving up.
    """
    import time

    from ddgs import DDGS

    query = args.get("query", "").strip()
    if not query:
        return "web_search error: no query given"

    last = f"No results for '{query}'."
    for attempt in range(3):
        try:
            results = list(DDGS().text(query, max_results=5))
            if results:
                lines = [f"Results for '{query}':"]
                for i, r in enumerate(results, 1):
                    lines.append(f"{i}. {r.get('title', '')}\n   "
                                 f"{r.get('body', '')}\n   {r.get('href', '')}")
                return "\n".join(lines)
        except Exception as exc:  # rate limit, network hiccup, etc.
            last = f"web_search error: {type(exc).__name__}: {exc}"
        time.sleep(1.5)
    return last


# The registry. The harness turns this into the `tools` list Claude sees.
# >>> Part C of the lab: add your new Tool to this list. <<<
BUILTIN_TOOLS: list[Tool] = [
    Tool(
        name="web_search",
        description=(
            "Search the web for current or factual information. Use this when "
            "the answer depends on recent events, specific facts, names, dates "
            "or figures you are not sure of. Not needed for general knowledge."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "What to search for"}
            },
            "required": ["query"],
        },
        run=_web_search,
    ),
]


def all_tools() -> list[Tool]:
    return list(BUILTIN_TOOLS)
