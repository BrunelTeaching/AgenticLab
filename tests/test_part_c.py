"""Part C — give the agent a second tool: a `calculator`.

The model is shaky at arithmetic, so give it a calculator for the numeric side
of event-hunting ("how many days until...", "is the ticket under £20"). Watch
the model choose between searching and calculating.

These tests are SKIPPED on the scaffold. Enable them by deleting the skip line
once you have registered a `calculator` tool in agent/tools.py. Reference
solution: solutions/tools_calculator.py.
"""

import pytest

pytest.skip("Enable in Part C: remove this line once you've added the tool.",
            allow_module_level=True)

from pathlib import Path  # noqa: E402

from agent import run  # noqa: E402
from agent.tools import all_tools  # noqa: E402

from tests.conftest_fakes import ScriptedModel, call_tool, say  # noqa: E402

WORKSPACE = Path(__file__).parent.parent / "workspace"


def test_calculator_is_registered():
    names = [t.name for t in all_tools()]
    assert "calculator" in names, "register a Tool named 'calculator' in tools.py"


def test_calculator_computes_correctly():
    calc = next(t for t in all_tools() if t.name == "calculator")
    assert "391" in calc.run({"expression": "17 * 23"})


def test_model_can_choose_the_calculator():
    model = ScriptedModel([
        call_tool("calculator", {"expression": "17 * 23"}),
        say("That's 391."),
    ])
    result = run("how many is 17 times 23?", WORKSPACE, call_model=model)
    assert result.trace[0]["tool"] == "calculator"
    assert "391" in result.answer
