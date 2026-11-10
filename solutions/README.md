# Solutions & instructor notes

Use these only to check your work or if you get stuck.

## The shape of the lab

The agent is an **events / hackathons finder** and deliberately ~40 lines so
students can read all of it: `agent/model.py` is the only LLM call,
`agent/harness.py` is the loop, `agent/tools.py` is the tools, `agent/memory.py`
loads `AGENTS.md`. The lesson is **an agent is a wrapper around a model** —
everything else is ordinary code.

## Part A — run it

- `python run.py "What is a hackathon?"` → the model answers from general
  knowledge, **one** model call, empty trace.
- `python run.py "AI hackathons for students in London this term"` → the model
  emits a `tool_use` for `web_search`; the harness runs it, feeds the result
  back, and the model answers with a short list (the format comes from
  `AGENTS.md`). Live results vary — that's the point of a real agent.

## Part B — memory

Edit `workspace/AGENTS.md`. Examples that visibly change behaviour: change "up to
3 events" to 5 and add a "why you'd go" line; add `- Only list events that are
free to attend.`; add `- Always answer in French.` No code changes. Without a
key, students can confirm the change reaches the model:

```
python -c "from pathlib import Path; from agent.memory import load_system_prompt; print(load_system_prompt(Path('workspace')))"
```

## Part C — add a tool

See `tools_calculator.py`. Paste `_calculator` (and its helpers) next to
`_web_search` in `agent/tools.py`, add the `Tool(...)` entry to `BUILTIN_TOOLS`,
then delete the skip line in `tests/test_part_c.py`.

```
python run.py "How many days are there in 7 weeks?"   # ACT calculator(...) -> 49
pytest -q                                             # -> 8 passed
```

The harness and the model call never changed — the new ability came entirely
from registering a tool, and the model now routes numbers → calculator, events →
search on its own.

## Expected baseline

`pytest -q` on the shipped scaffold: **5 passed, 1 skipped** (Part C). After the
student enables Part C: **8 passed**. All tests run offline via the scripted
model in `tests/conftest_fakes.py`.

## Running without keys (whole class)

Only `python run.py` needs `GROQ_API_KEY`. The tests, the loop dissection
(Part A reading), the memory inspection (Part B one-liner), and the tool wiring
(Part C) all work with no key. If keys are scarce, demo the live runs from the
front and have students do B and C against the tests.

## Part D (stretch) notes

- **Add `read_page` (the real two-step loop):** `tools_read_page.py` is included
  and ready; paste it in the same way. The agent then does `search → open the best
  result → read its date/venue`, showing a genuine search-then-read loop.
- **Swap the model:** e.g. `MODEL = "openai/gpt-oss-20b"` in `agent/model.py`, or
  a different provider via BASE_URL + MODEL + key (e.g. Google Gemini).
- **Break the loop:** comment out the tool-execution block in `harness.py`; the
  model keeps asking for tools but nothing runs them — shows the harness is what
  makes tools real.
