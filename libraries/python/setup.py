from setuptools import setup, find_packages

setup(
    name="GCI",
    version="0.1.0",
    description="A Unified Numerical Metric for Algorithmic Complexity",
    long_description="Reference implementation for the Geometric Complexity Metric (GCI), a geometric phase space for static analysis.",
    author="Harry Bullman",
    author_email="harrybullmandy@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    keywords="complexity, static-analysis, big-o, physics",
    # --- ADD THIS SECTION ---
    entry_points={
        "console_scripts": [
            "gci-scan=GCI.cli:main",  # Changed from 'GCI' to 'gci-scan'
        ],
    },
    # ------------------------
)
