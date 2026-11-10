"""The HARNESS — the loop that turns a model into an agent.

From the lecture: *an agent is a language model that uses tools in a loop to
reach a goal.* This file is that loop, and it is about a dozen lines of real
work. Read it alongside the "under the hood" slide — it is the same shape used
inside Claude Code and opencode:

    messages = [the memory (system), the user's question]
    repeat:
        reply = call the model with (messages, tools)   # THINK
        if the model asked for a tool:
            run the tool, append its result to messages  # ACT + OBSERVE
        else:
            return the model's answer                    # DONE

The model decides *what* to do; this code only carries it out and feeds the
result back. Take the model away (agent/model.py) and nothing here can think —
that's the point of the lab: the agent is a wrapper around a model.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .memory import load_system_prompt
from .model import call_model as real_call_model
from .tools import Tool, all_tools


@dataclass
class Result:
    answer: str
    trace: list[dict] = field(default_factory=list)   # the tool calls that happened


# Stop offering tools after this many calls, so the agent can't loop forever
# searching — it must then answer. This also caps how hard a whole class hits
# the web_search back-end at once.
TOOL_BUDGET = 3


def run(
    question: str,
    workspace: Path,
    call_model: Callable = real_call_model,
    tools: list[Tool] | None = None,
    max_steps: int = 6,
    log: Callable[[str], None] = lambda _msg: None,
) -> Result:
    """Answer one question, using tools in a loop if the model asks to.

    ``call_model`` and ``tools`` are injectable so the tests can run offline
    with a scripted model and fake tools; the defaults use the real (free) model
    call and the real web_search tool.
    """
    tools = all_tools() if tools is None else tools
    by_name = {t.name: t for t in tools}
    tool_schemas = [t.schema() for t in tools]

    messages: list = [
        {"role": "system", "content": load_system_prompt(workspace)},
        {"role": "user", "content": question},
    ]
    trace: list[dict] = []
    answer = ""

    log(f"QUESTION  {question}\n")

    for step in range(1, max_steps + 1):
        # Once the search budget is spent, tell the model to stop and answer.
        # (We keep the tools in the request so the provider doesn't reject it, but
        # the model reliably replies in plain text when asked.)
        over_budget = len(trace) >= TOOL_BUDGET
        if over_budget:
            messages.append({"role": "user",
                             "content": "You have used your search budget. Answer now "
                                        "in plain text from what you've found. Do not "
                                        "call any tool."})

        reply = call_model(messages, tool_schemas)               # THINK
        message = reply.choices[0].message
        messages.append(message)                                 # remember what it said

        said = (message.content or "").strip()
        if said:
            log(f"STEP {step}  THINK   {said}")

        tool_calls = message.tool_calls or []
        if over_budget or not tool_calls:
            answer = said
            break

        for call in tool_calls:                                  # ACT
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            tool = by_name.get(name)
            output = tool.run(args) if tool else f"unknown tool: {name}"
            log(f"STEP {step}  ACT     {name}({args})")
            log(f"STEP {step}  OBSERVE {output.splitlines()[0] if output else ''}")
            trace.append({"tool": name, "input": args, "output": output})
            messages.append(                                     # OBSERVE
                {"role": "tool", "tool_call_id": call.id, "content": output}
            )

    if not answer:
        answer = "(couldn't put together an answer this time — try running it again)"

    log(f"\nANSWER\n{answer}")
    return Result(answer=answer, trace=trace)
