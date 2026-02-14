# **The Geometric complexity Index (GCI)**

**A Unified Numerical Metric for Algorithmic Complexity**

## **🚨 The Problem: Big O is "Low Resolution"**

In standard complexity theory, a n algorithm with $50n$ operations and one with $n$ operations are both labeled $O(n)$. This ignores the physical reality of computing: **Constants matter.**

Similarly, there is no numerical way to measure "Technical Debt." You cannot say, _"This_ commit made the _code 15% more complex."_ You can only say, _"It's still Polynomial."_

## **💡 The Solution: The Functional Phase Space**

The **Geometric Complexity Index (GCI)** is a static analysis standard that converts abstract complexity labels into precise, continuous scalar scores.

It maps algorithms into a **3D Phase Space** defined by:

1. **Rank ($Z$):** The class of operation (Polynomial vs. Exponential).
2. **Magnitude ($X$):** The "Inertial Mass" (Static instruction count / Bit density).
3. **Rate ($Y$):** The "Kinetic Curvature" (Exponent).

By utilizing **Level-Index Arithmetic**, it calculates a **Gradient** Magnitude that allows for the comparison of hyper-exponential structures without causing computational overflow.

## **🚀 Quick Start**

### **Installation**

This repository contains the reference Python implementation.

```bash
git clone https://github.com/squarewatermeln/GCI.git
cd GCI
```

### **Usage**

Calculate the **Standard Geometric Complexity Score ($GCI_{1M}$)**. This metric standardizes the load at $x = 10^6$ (1 Million inputs) to identify bottlenecks under industrial stress.

```bash
\# Analyze a heavy linear function (50n)
\# Rank=2 (Poly), Magnitude=50, Rate=1
python src/metric.py \--rank 2.0 \--mag 50.0 \--rate 1.0
```

**Output:**

```bash
\--- Analysis for Standard Load x=1,000,000 \---
Coordinate:     (R=2.0, M=50.0, Rate=1.0)
Projected Cost: 5.0000e+07 ops
Score:  3.268 GCI (Standard)
```

### **Comparison**

Compare that to a "Light Quadratic" function ($n^2/10$) which Big O usually penalizes more:

```bash
\# Analyze n^2 / 10
python src/metric.py \--rank 2.0 \--mag 0.1 \--rate 2.0
```

**Output:**

```bash
Score: 3.522 GCI
```

_Result:_ The metric correctly identifies that for $10^6$ inputs, the quadratic function is indeed heavier, but provides a precise numerical distance ($\Delta = 0.254$ GCI) rather than a vague label.

## **📐 The Coordinate System**

The metric projects four functional tensors into a visible 3D manifold:

| Axis  | Name          | Physics Metaphor      | Description                                      |
| :---- | :------------ | :-------------------- | :----------------------------------------------- |
| **Z** | **Rank**      | **Potential Energy**  | The Hyper-operation level ($2=$ Poly, $3=$ Exp). |
| **X** | **Magnitude** | **Inertial Mass**     | The static weight ($A$ in $A \cdot n^B$).        |
| **Y** | **Rate**      | **Kinetic Curvature** | The growth exponent ($B$ in $n^B$).              |

### **The "Geometric Complexity" Unit (GCI)**

The **GCI** is a logarithmic unit of computational weight.

- **1.0 GCI:** Linear Baseline.
- **3.0 GCI:** The "Event Horizon" between Polynomial and Exponential complexity.
- **4.0+ GCI:** Hyper-recursive / Tetration risk (System Crash likely).

## **🧪 Case Study**

| Algorithm           | Big O        | Coordinate            | Score (GCI1M​) |
| :------------------ | :----------- | :-------------------- | :------------- |
| **Linear Search**   | **$O(n)$**   | **$(2.0, 1.0, 1.0)$** | **3.14 GCI**   |
| **Bubble Sort**     | **$O(n^2)$** | **$(2.0, 1.0, 2.0)$** | **3.44 GCI**   |
| **Naive Fibonacci** | **$O(2^n)$** | **$(3.0, 2.0, 1.0)$** | **4.14 GCI**   |

## **🤝 Contributing**

This is a **Reference Implementation**. We are actively looking for contributors to build:

1. **Parsers:** Tools to extract $(R, X, Y)$ coordinates from source code automatically (AST analysis).
2. **Visualizers:** Web-based 3D plotters for the Phase Space.
3. **Ports:** Implementations in Rust, Go, and TypeScript.

**Pull Requests are welcome.**

## **📜 Citation**

If you use this metric in your research or tooling, please cite the whitepaper:

```
Title: The Geometric Complexity Index
Publication: Zenodo (Pre-print)
DOI: 10.5281/zenodo.18640728
Link: https://doi.org/10.5281/zenodo.18640728
```

**Author:** Harry Bullman
_Independent Researcher_
