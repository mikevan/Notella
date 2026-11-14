[Tutorial index](index.md) · [Windows setup](setup-windows.md) · [macOS/Linux setup](setup-macos-linux.md)

# Tutorial 0: set up your environment

Start here before running any Notella tutorial. You will obtain the source, create an isolated Python environment, and verify a complete curriculum example. No existing workspace, GPU, model, API key, or paid account is assumed.

## Choose your platform

- [Windows setup](setup-windows.md): PowerShell, a local source folder, and a project-specific Python interpreter.
- [macOS or Linux setup](setup-macos-linux.md): Terminal, a local source folder, and a project-specific Python interpreter.

Each guide explains installation, expected results, returning to the project later, and common errors. Use one guide, then continue to [Tutorial 1](tutorial.md).

## What the setup proves

The core tutorials run on Python 3.11 or later using the standard library. The setup checks run the test suite and an authored fixture. A successful result verifies the local workflow; it does not train a model or measure semantic accuracy. After initial source and Python downloads, these core exercises can run offline.

Training is a separate environment. [Tutorial 4](training.md) describes the current CUDA backend, its pinned packages, and licensed local model requirements. A Mac can run the core tutorials, but this training backend does not provide an Apple Metal or CPU training path. A Python version suitable for the core does not guarantee compatibility with the pinned GPU stack.

## Read commands in the right place

Run commands from the project root: the folder containing `notella`, `examples`, `tests`, and `pyproject.toml`. Your chosen folder replaces example locations such as `C:\workspace\Notella`; you do not need the author's directory layout.

Use the interpreter created by your platform guide whenever a tutorial says `python`:

| Platform | Project interpreter |
| --- | --- |
| Windows PowerShell | `.\.venv\Scripts\python.exe` |
| macOS or Linux | `./.venv/bin/python` |

PowerShell blocks belong in PowerShell; `sh` blocks belong in Terminal. Python blocks belong in a `.py` file or a Python session. Platform setup explains how to save and run the shared Python snippets. Shell syntax is not interchangeable: `$env:NAME = 'value'` in PowerShell becomes `export NAME='value'` in bash/zsh, and `Set-Location` becomes `cd`.

## Continue

[Open the tutorial index](index.md) for the complete sequence, or read [how we use and train AI](how-we-use-ai.md) before running it.

---

[Previous: tutorial index](index.md) · [Next: Tutorial 1 — Your first semantic curriculum](tutorial.md)
