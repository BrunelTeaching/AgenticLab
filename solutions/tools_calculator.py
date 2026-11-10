"""Reference solution for Part C — the `calculator` tool.

Copy `_calculator` next to `_web_search` in agent/tools.py, and add the Tool(...)
entry to BUILTIN_TOOLS. Then delete the skip line in tests/test_part_c.py.

It evaluates a maths expression safely (no `eval`) by walking the parse tree, so
the agent can do arithmetic the model would otherwise get wrong.
"""

import ast
import operator

from agent.tools import Tool

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.Pow: operator.pow, ast.USub: operator.neg, ast.Mod: operator.mod,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")


def _calculator(args: dict) -> str:
    expr = args.get("expression", "")
    try:
        return f"{expr} = {_eval(ast.parse(expr, mode='eval').body)}"
    except Exception as exc:
        return f"calculator error: {exc}"


CALCULATOR_TOOL = Tool(
    name="calculator",
    description="Evaluate an arithmetic expression, e.g. '17 * 23'. Use this for "
                "any maths rather than working it out yourself.",
    input_schema={
        "type": "object",
        "properties": {"expression": {"type": "string", "description": "e.g. 17 * 23"}},
        "required": ["expression"],
    },
    run=_calculator,
)
