import ast
import inspect
import textwrap
from typing import Union, Callable
from .metric import GCIMath


class ComplexityVisitor(ast.NodeVisitor):
    """
    Walks the Abstract Syntax Tree (AST) of a Python function
    to estimate Functional Phase Space coordinates.
    """

    def __init__(self):
        self.max_depth = 0  # Maps to Rate (Y)
        self.current_depth = 0
        self.operations = 0  # Maps to Magnitude (X)
        self.has_recursion = False
        self.func_name = None

    def visit_FunctionDef(self, node):
        if self.func_name is None:
            self.func_name = node.name
        self.generic_visit(node)

    def visit_For(self, node):
        self._enter_loop(node)

    def visit_While(self, node):
        self._enter_loop(node)

    def _enter_loop(self, node):
        self.current_depth += 1
        # Track maximum nesting depth (e.g., nested loops = depth 2)
        if self.current_depth > self.max_depth:
            self.max_depth = self.current_depth
        self.generic_visit(node)

    def visit_Call(self, node):
        self.operations += 1
        # Simple recursion detection: calling self
        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
            self.has_recursion = True
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # Count math operations (e.g., a + b)
        self.operations += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Count variable assignments
        self.operations += 1
        self.generic_visit(node)


def scan_function(target: Union[str, Callable]) -> dict:
    """
    Analyzes a Python function (or source string) and returns its GCI Metrics.

    Args:
        target: Either a raw code string OR a Python function object.

    Returns:
        dict: Containing the function name, coordinate, and GCI score.
    """
    source_code = ""

    # 1. Extract Source Code
    if isinstance(target, str):
        source_code = target
    elif callable(target):
        try:
            raw_source = inspect.getsource(target)
            # Remove common leading whitespace (fix indentation errors)
            source_code = textwrap.dedent(raw_source)
        except OSError:
            return {
                "error": "Could not retrieve source code (function might be defined dynamically)."
            }
        except TypeError:
            return {"error": "Target must be a function, method, or code string."}
    else:
        return {"error": "Invalid input. Must be a function or a string."}

    # 2. Parse AST
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {"error": "Invalid Python Syntax"}

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    # --- HEURISTIC MAPPING ---

    # 1. Determine Rank (Z)
    # Recursion is inherently Exponential Risk (Rank 3)
    # Loops imply Polynomial (Rank 2)
    # No loops imply Linear/Log (Rank 1)
    if visitor.has_recursion:
        rank = 3.0
    elif visitor.max_depth > 0:
        rank = 2.0
    else:
        rank = 1.0

    # 2. Determine Rate (Y) -> Loop Depth
    rate = max(1.0, float(visitor.max_depth))

    # 3. Determine Magnitude (X) -> Static Instruction Estimation
    magnitude = max(1.0, float(visitor.operations))

    # 4. Calculate Score
    score = GCIMath.calculate_score(rank, magnitude, rate)

    return {
        "function": visitor.func_name,
        "coordinate": (rank, magnitude, rate),
        "GCI": score,
        "details": {
            "nested_loops": visitor.max_depth,
            "instruction_est": visitor.operations,
            "recursive": visitor.has_recursion,
        },
    }
