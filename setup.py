#!/usr/bin/env python3

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="automation-entities",
    version="0.1.0",
    description="library for coloring automated routines for maximum debugability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SudoVim/automation-entities",
    author="Michael Renken",
    author_email="michaelarenken@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="automation",
    packages=[
        "automation_entities",
        "automation_entities.web_browser",
    ],
    python_requires=">=3.8, <4",
    install_requires=[
        "selenium>=4",
        "requests>=2",
        "assertpy>=1",
    ],
    project_urls={
        "Bug Reports": "https://github.com/SudoVim/automation-entities/issues",
        "Source": "https://github.com/SudoVim/automation-entities/",
    },
)
