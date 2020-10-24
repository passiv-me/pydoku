"""Copyright (C) 2020 Sivam Pasupathipillai <s.pasupathipillai@unitn.it>.

All rights reserved.
"""
from setuptools import setup, find_packages

setup(
    name="pydoku",
    version="0.1.0",
    description="Visual sudoku solver",
    author="Sivam Pasupathipillai",
    author_email="sivam.pasupathipillai@gmail.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["pydoku = pydoku.main:main"]},
)
