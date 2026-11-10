"""A tiny research agent for CS3616 — an LLM wrapped in a tool-using loop.

The components from the lecture, kept deliberately small so you can read them:
  model.py    - the only call to the LLM (the agent is a wrapper around this)
  memory.py   - MEMORY: workspace/AGENTS.md goes into the system prompt
  tools.py    - TOOLS: web_search (+ whatever you add in Part C)
  harness.py  - the Think -> Act -> Observe loop that ties them together
"""

from .harness import Result, run

__all__ = ["run", "Result"]
