# GCI A Unified Numerical Metric for Algorithmic Complexity

VERSION 0.1.0

DESCRIPTION The Geometric complexity Metric (GCI) provides a geometric phase space for static code analysis. Unlike Big-O notation, which describes asymptotic behavior, the GCI Metric calculates a concrete "Industrial Load" score based on the structure of the code itself.

It maps code into three dimensions:

Magnitude (X): The raw volume of operations (assignments, math, calls).

Rate (Y): The nesting depth of the logic (loop intensity).

Rank (Z): The fundamental complexity class (Linear, Polynomial, or Recursive/Exponential).

INSTALLATION Navigate to the root directory and install via pip: pip install .

USAGE You can scan code by passing raw strings or actual Python function objects.

Example:

```python
from GCI import scan_function
```

## Define a function to test

```python
def calculate_fib(n):
    if n <= 1: return n
    return calculate_fib(n-1) + calculate_fib(n-2)
```

## Scan the function directly

```python
result = scan_function(calculate_fib)

print(f"GCI Score: {result['GCI_score']}")
print(f"Coordinates: {result['coordinate']}")
```

## INTERPRETING THE SCORE

$GCI_1M$ (Standard GCI Score) is normalized against a standard load of 1,000,000 operations.

Scores are logarithmic. A small increase in score represents a significant jump in computational cost.

Coordinate format: (Rank, Magnitude, Rate)

## INSTALLATION

```bash
cd /libraries/python
pip install .
```

AUTHOR Harry Bullman
