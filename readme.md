# Sparx Reader Solver

A small python script connecting to an ollama interface which starts sparx homework, answers questions about the text, bypasses cheating prevention measures and doesn't trigger the cheating marker on the teacher dashboard.

## Features

- Decision model support
- Text dependant speed
- Automatic starting
- Answers difficulty checks
- Saves login information

## Install

> Must have ollama 0.35.0 or higher

``` bash
python -m venv .venv
pip install requirements.txt
playwright install firefox
ollama pull tev1:4b
python main.py
```
