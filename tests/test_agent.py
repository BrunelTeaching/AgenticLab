"""Baseline tests — run offline, no API key, no network.

They use a scripted stand-in model (tests/conftest_fakes.py) so they check the
*agent* — the loop, the memory, the tools — without calling a real model. These
are the tests you keep green while you change the agent in Parts B and C.
"""

from pathlib import Path

from agent import run
from agent.memory import load_system_prompt
from agent.tools import Tool, all_tools

from tests.conftest_fakes import ScriptedModel, call_tool, say

WORKSPACE = Path(__file__).parent.parent / "workspace"


def _fake_tool(name="web_search", output="FAKE RESULT"):
    return Tool(name, "fake", {"type": "object", "properties": {}}, lambda args: output)


def test_answers_directly_when_no_tool_is_needed():
    # The model replies with plain text and no tool call -> the loop stops.
    model = ScriptedModel([say("Paris.")])
    result = run("capital of France?", WORKSPACE, call_model=model, tools=[_fake_tool()])
    assert result.answer == "Paris."
    assert result.trace == []
    assert len(model.calls) == 1


def test_uses_a_tool_then_answers():
    # Step 1: model asks for web_search. Step 2: model answers using the result.
    model = ScriptedModel([
        call_tool("web_search", {"query": "brunel"}),
        say("Brunel is in Uxbridge."),
    ])
    result = run("where is brunel?", WORKSPACE, call_model=model,
                 tools=[_fake_tool(output="Brunel University London is in Uxbridge.")])
    assert result.answer == "Brunel is in Uxbridge."
    assert len(result.trace) == 1
    assert result.trace[0]["tool"] == "web_search"


def test_tool_result_is_fed_back_to_the_model():
    # The second model call must see the tool result in the conversation.
    model = ScriptedModel([
        call_tool("web_search", {"query": "x"}),
        say("done"),
    ])
    run("q", WORKSPACE, call_model=model, tools=[_fake_tool(output="THE RESULT")])
    second_call_messages = model.calls[1]["messages"]
    dumped = str(second_call_messages)
    assert "THE RESULT" in dumped
    assert "'role': 'tool'" in dumped


def test_memory_is_in_the_system_prompt():
    # The persona and rules from AGENTS.md must reach the model's system prompt.
    system = load_system_prompt(WORKSPACE)
    assert "Scout" in system
    assert "web_search" in system


def test_web_search_tool_has_a_valid_schema():
    web = next(t for t in all_tools() if t.name == "web_search")
    schema = web.schema()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "web_search"
    assert schema["function"]["parameters"]["required"] == ["query"]
