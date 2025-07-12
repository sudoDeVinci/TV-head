#!/usr/bin/env python3
"""
Setup script for TV Head project.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="tv-head",
    version="1.0.0",
    author="Tadj Cazaubon",
    author_email="your.email@example.com",
    description="LED matrix display controller for TV Head cosplay",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sudoDeVinci/TV-head",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0", 
        "toml>=0.10.0",
    ],
    extras_require={
        "sprites": ["pygame>=2.0.0"],
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
        "docs": ["Sphinx>=3.0.0"],
    },
    entry_points={
        "console_scripts": [
            "tvhead=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.toml", "*.md", "*.txt"],
    },
    zip_safe=False,
)
