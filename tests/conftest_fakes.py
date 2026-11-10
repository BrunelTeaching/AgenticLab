"""Tiny fakes so the tests run offline, with no API key and no network.

A real reply from an OpenAI-compatible model is ``reply.choices[0].message``,
where the message has ``.content`` (text) and ``.tool_calls`` (a list, each with
``.id`` and ``.function.name`` / ``.function.arguments``). We mimic just enough
of that shape here so the harness can't tell the difference — which also shows
how little the harness assumes about the model.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class FakeFunction:
    name: str
    arguments: str          # a JSON string, exactly like the real API


@dataclass
class FakeToolCall:
    function: FakeFunction
    id: str = "call_fake"
    type: str = "function"


@dataclass
class FakeMessage:
    content: str | None = None
    tool_calls: list | None = None


@dataclass
class FakeChoice:
    message: FakeMessage


@dataclass
class FakeReply:
    choices: list = field(default_factory=list)


def say(text: str) -> FakeReply:
    """A reply that is just a final answer (no tool call)."""
    return FakeReply([FakeChoice(FakeMessage(content=text))])


def call_tool(name: str, args: dict) -> FakeReply:
    """A reply that asks the harness to run one tool."""
    tc = FakeToolCall(FakeFunction(name=name, arguments=json.dumps(args)))
    return FakeReply([FakeChoice(FakeMessage(content=None, tool_calls=[tc]))])


class ScriptedModel:
    """A stand-in for call_model that returns pre-written replies in order."""

    def __init__(self, replies: list[FakeReply]):
        self.replies = replies
        self.calls: list[dict] = []

    def __call__(self, messages, tools):
        self.calls.append({"messages": messages, "tools": tools})
        return self.replies[min(len(self.calls) - 1, len(self.replies) - 1)]
