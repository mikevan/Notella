[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 0: set up a Windows test environment

**Outcome:** a local copy of Notella, an isolated Python environment, and a successful first curriculum run. Start here even if you have never used Python. These steps prepare the core tutorials; model training has additional requirements.

You need a Windows computer, an internet connection for the initial downloads, permission to install Python, and a writable folder in your user account. No GPU, model weights, API key, paid account, or existing dataset is needed. Once Python and the source are present, the core tutorial runs offline.

## 1. Install Python

Open the official [Python for Windows download page](https://www.python.org/downloads/windows/) and follow its installation instructions. Install a stable Python 3.11 or later, rather than a prerelease. If using the Python install manager, install a Python runtime as well as the manager.

Open **Start**, type **PowerShell**, and open it. You do not need an administrator terminal. Enter:

```powershell
py --version
```

Expect `Python 3.11` or a newer version. If `py` is unavailable, try `python --version`. If that works, use `python` instead of `py` when creating the environment in step 3. If neither works, finish Python's installation and open a new PowerShell window before trying again.

## 2. Get the Notella source

Open the [Notella repository](https://github.com/mikevan/Notella) in your browser. Sign in if your copy requires repository access. Choose **Code → Download ZIP**, then use File Explorer's **Extract All** command. If you cannot access the repository, obtain access or a source ZIP from the project maintainer before continuing.

Create a folder named `Notella` inside your user folder and put the extracted project contents there. The result should include `docs`, `examples`, `notella`, `tests`, and `pyproject.toml` directly inside `Notella`; avoid an extra nested `Notella-main` folder. Your user folder is usually `C:\Users\your-name` and is available from File Explorer's address bar as `%USERPROFILE%`.

In PowerShell, enter:

```powershell
Set-Location "$env:USERPROFILE\Notella"
Get-ChildItem
```

Confirm that the files and folders listed above appear. If you chose a different location, use its full path in quotes instead. This folder is the **project root**: run the tutorial commands here.

## 3. Create a separate Python environment

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import sys; print(sys.executable)"
```

The last command should print a path ending in `Notella\.venv\Scripts\python.exe`. This environment belongs to this project and keeps its Python packages separate. See Python's [virtual environment documentation](https://docs.python.org/3/library/venv.html).

Use the explicit environment path shown here. Activation is optional, so no PowerShell execution-policy change is needed. The core runs directly from the project root without a package installation or dependency download.

## 4. Check the environment and run the example

Run these commands one at a time. Stop if either reports an error.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m examples.tutorial --store runtime/tutorial
```

The tests should end with `OK`. The example should print four artifact IDs, splits of `train: 3`, `validation: 1`, `test: 1`, and these flags:

```json
{
  "fixtureOnly": true,
  "modelLoaded": false,
  "trainingStarted": false,
  "semanticAccuracyMeasured": false
}
```

Confirm the saved result:

```powershell
Get-Content runtime/tutorial/tutorial-result.json
```

Notella creates `runtime/tutorial` for you. A successful run verifies the local curriculum workflow; it does not train or assess a model.

Verified on Windows with a fresh Python 3.14.2 environment on November 14, 2026: 154 core tests and the first example passed without additional packages, model loading, or training. This verifies that environment, not every Windows/Python combination.

## 5. Continue with Tutorial 1

Open [Tutorial 1](tutorial.md). Whenever it says `python`, use `.\.venv\Scripts\python.exe` in this PowerShell window.

For its Python snippets, open Notepad or another plain-text editor. Create `tutorial_walkthrough.py` in the project root, paste the Python snippets in their displayed order, save, and run:

```powershell
.\.venv\Scripts\python.exe tutorial_walkthrough.py
```

Make sure the filename ends in `.py`, not `.py.txt`. PowerShell blocks are terminal commands; Python blocks go in the script. The Python snippets share variables, so keep them together and in order.

When returning later, open PowerShell, change to your project folder again, and use the same `.venv` interpreter. You do not need to recreate it.

## If a check fails

- **Python opens the Microsoft Store or is not found:** finish installing a Python runtime, reopen PowerShell, and try `py --version` again.
- **No module named `notella` or `examples`:** check that you are in the folder containing both directories, rather than its parent or `docs`.
- **Access denied:** use a folder owned by your user account; avoid `Program Files` or other protected locations.
- **A test fails:** retain the error output and resolve it before proceeding. See [troubleshooting](troubleshooting.md).

---

[Previous: Tutorial 0 — choose your environment](setup.md) · [Next: Tutorial 1 — your first semantic curriculum](tutorial.md)
