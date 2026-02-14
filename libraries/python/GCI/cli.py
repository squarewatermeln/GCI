import argparse
import ast
import sys
import os
from .scanner import scan_node


def analyze_file(filepath):
    """Parses a file and runs GCI on every function definition found."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Error: Syntax error in '{filepath}': {e}")
        return
    except Exception as e:
        print(f"Error reading '{filepath}': {e}")
        return

    print(f"\nScanning: {filepath}")
    print("-" * 60)
    print(f"{'FUNCTION':<25} | {'COORD (Z, X, Y)':<15} | {'GCI SCORE':<10}")
    print("-" * 60)

    functions_found = False

    # Walk the file's AST to find FunctionDefs
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef, ast.AsyncFunctionDef):
            functions_found = True
            # Scan the individual function node
            result = scan_node(node)

            name = result["function"]
            # Format coordinate as (Rank, Mag, Rate)
            coord = f"({result['coordinate'][0]:.0f}, {result['coordinate'][1]:.0f}, {result['coordinate'][2]:.0f})"
            score = f"{result['GCI']:.4f}"

            print(f"{name:<25} | {coord:<15} | {score:<10}")

    if not functions_found:
        print("No functions found in file.")
    print("-" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="GCI: Geometric Complexity Interface")
    parser.add_argument("path", help="Path to the Python file to scan")

    args = parser.parse_args()
    analyze_file(args.path)


if __name__ == "__main__":
    main()


# TODO: add async walker for classes
