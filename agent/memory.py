"""Component: MEMORY — what the agent knows before it reads your question.

The agent's **project memory** lives in workspace/AGENTS.md. It is loaded once
and placed in the model's *system prompt* — the standing instructions the model
sees on every call. Editing AGENTS.md changes how the agent behaves (its name,
its style, whether it cites sources) with no change to any code. That is exactly
how real agents work: Claude Code reads CLAUDE.md, many tools read AGENTS.md.

The short base prompt below only tells the model it has tools and should decide
when to use them; everything *steerable* lives in AGENTS.md, so Part B can change
the agent by editing a text file.
"""

from __future__ import annotations

from pathlib import Path

BASE_PROMPT = (
    "You help students find upcoming tech events, hackathons and meetups. You have "
    "a web_search tool. When the user tells you their interests and location, search "
    "the web for relevant upcoming events and give them a short, useful shortlist. "
    "Decide for yourself when a request needs a search and when you can answer "
    "directly. Follow the project rules below."
)


def load_system_prompt(workspace: Path) -> str:
    """Base instructions + the project memory from AGENTS.md."""
    agents_md = workspace / "AGENTS.md"
    memory = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    return f"{BASE_PROMPT}\n\n# Project memory (AGENTS.md)\n{memory}"
