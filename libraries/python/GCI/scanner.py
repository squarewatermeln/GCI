import ast
import inspect
import textwrap
from typing import Union, Callable, Any
from .metric import GCIMath


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0
        self.operations = 0
        self.has_recursion = False
        self.func_name = None

    def visit_FunctionDef(self, node):
        if self.func_name is None:
            self.func_name = node.name
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_For(self, node):
        self._enter_loop(node)

    def visit_While(self, node):
        self._enter_loop(node)

    def _enter_loop(self, node):
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
        self.generic_visit(node)
        self.current_depth -= 1  # IMPORTANT: Decrement when leaving the loop

    def visit_Call(self, node):
        self.operations += 1
        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
            self.has_recursion = True
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.operations += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.operations += 1
        self.generic_visit(node)


def _calculate_metrics(visitor: ComplexityVisitor) -> dict:
    """Internal helper to calculate GCI from a populated visitor."""
    # 1. Determine Rank (Z)
    if visitor.has_recursion:
        rank = 3.0
    elif visitor.max_depth > 0:
        rank = 2.0
    else:
        rank = 1.0

    # 2. Determine Rate (Y)
    rate = max(1.0, float(visitor.max_depth))

    # 3. Determine Magnitude (X)
    magnitude = max(1.0, float(visitor.operations))

    # 4. Calculate Score
    score = GCIMath.calculate_score(rank, magnitude, rate)

    return {
        "function": visitor.func_name or "anonymous",
        "coordinate": (rank, magnitude, rate),
        "GCI": score,
        "details": {
            "nested_loops": visitor.max_depth,
            "instruction_est": visitor.operations,
            "recursive": visitor.has_recursion,
        },
    }


def scan_node(node: ast.AST) -> dict:
    """Scans a raw AST node (used by CLI)."""
    visitor = ComplexityVisitor()
    visitor.visit(node)
    return _calculate_metrics(visitor)


def scan_function(target: Union[str, Callable]) -> dict:
    """Analyzes a Python function (or source string)."""
    source_code = ""
    if isinstance(target, str):
        source_code = target
    elif callable(target):
        try:
            raw_source = inspect.getsource(target)
            source_code = textwrap.dedent(raw_source)
        except (OSError, TypeError):
            return {"error": "Could not retrieve source code."}
    else:
        return {"error": "Invalid input."}

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {"error": "Invalid Python Syntax"}

    visitor = ComplexityVisitor()
    visitor.visit(tree)
    return _calculate_metrics(visitor)
