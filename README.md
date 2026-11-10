# CS3616 — Agentic SE Lab: Dissect an Agent

A 30–40 minute lab for *Introduction to Agentic Software Engineering* (Lecture 1).

**What the agent is, in one line:** an events finder — you tell it your interests
and your city, and it searches the web for upcoming tech events, hackathons and
meetups and gives you a short list with dates, venues and sign-up links.

You take it apart: ~40 lines of Python — a **loop**, some **tools**, a
**memory** file — wrapped around **one call to a free real model** (gpt-oss on
Groq). You run it, watch it decide to search the web, then change what it does by
editing its memory and giving it a new tool.

The point: an agent is a *wrapper around a model*. Everything else is ordinary
code you can read. This is the honest, smallest version of what Claude Code and
opencode do.

## Start here

1. Play the warm-up: open **`instructions/Concept_Game.html`** in a browser.
2. Do the lab: open **`instructions/Lab_Instructions.html`** for the full walkthrough.

## Quick start

```bash
git clone https://github.com/BrunelTeaching/AgenticLab.git
cd AgenticLab
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
bash check.sh                      # offline tests — 5 passed, 1 skipped (no key needed)

export GROQ_API_KEY=gsk_...                 # class key, or a free one at https://console.groq.com
python run.py "What is a hackathon?"                        # answers, no search
python run.py "AI hackathons for students in London this term"   # searches the web
```

The model is `openai/gpt-oss-120b` on Groq's free tier. `agent/model.py` uses the
OpenAI-compatible API, so you can point it at any other provider (Groq's other
free models, Google Gemini, OpenAI, a local Ollama) by changing the base URL,
model string and key.

## Layout

```
run.py                   # ask the agent what's on, watch the loop
agent/model.py           # the ONLY call to the LLM — the agent wraps this
agent/memory.py          # MEMORY: workspace/AGENTS.md → the system prompt
agent/tools.py           # TOOLS: web_search (+ what you add in Part C)
agent/harness.py         # the Think → Act → Observe LOOP (~a dozen lines)
workspace/AGENTS.md      # the agent's memory (edited in Part B)
tests/test_agent.py      # offline baseline (scripted model, no key/network)
tests/test_part_c.py     # Part C tests (skipped until you enable them)
tests/conftest_fakes.py  # a fake model so tests run offline
solutions/               # reference answers — peek only if stuck
```

## The parts

| Part | Topic | What you do |
|------|-------|-------------|
| Warm-up | Concepts | Play the 5-round concept game |
| 0 | Setup | Install, run the offline tests, set your key |
| A | The loop | Run it; see the model search for one request, not another; find the model call inside the agent |
| B | **Memory** | Change the agent (name, style, language) by editing `AGENTS.md` — no code change |
| C | **Tools** | Add a `calculator` tool; watch the model pick between searching and calculating |
| D | Stretch | Add a `read_webpage` tool, swap the model, or break the loop to see where the intelligence lives |

Baseline: `pytest -q` → **5 passed, 1 skipped**. After Part C → **8 passed**.
The tests run fully offline (a scripted stand-in model); only `python run.py`
needs an API key.
