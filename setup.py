"""Copyright (C) 2020 Sivam Pasupathipillai <s.pasupathipillai@unitn.it>.

All rights reserved.
"""
from setuptools import setup, find_packages

with open("requirements.txt", "r") as requirements_file:
    install_requirements = [line for line in requirements_file] 

setup(
    name="sudoku",
    version="0.1.0",
    description="Visual sudoku solver",
    author="Sivam Pasupathipillai",
    author_email="sivam.pasupathipillai@gmail.com",
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        "console_scripts": ["pydoku = sudoku.main:main"]
    }
)