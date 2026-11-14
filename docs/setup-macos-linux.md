[Tutorial index](index.md) · [Tutorial 0: environment setup](setup.md)

# Tutorial 0: set up a macOS or Linux test environment

**Outcome:** a local copy of Notella, an isolated Python environment, and a successful first curriculum run. No existing Python workspace is assumed. These steps prepare the core tutorials; model training has additional requirements.

You need an internet connection for initial downloads, permission to install Python if needed, and a writable folder in your home directory. No GPU, model weights, API key, paid account, or existing dataset is needed. Once Python and the source are present, the core tutorial runs offline.

## 1. Open a terminal and check Python

On macOS, open **Terminal** from Applications → Utilities. On Linux, open your desktop's Terminal application. The commands below use bash/zsh syntax.

```sh
python3 --version
```

Use stable Python 3.11 or later. If the command is missing or reports an older version:

- **macOS:** install a suitable version from the official [Python macOS downloads](https://www.python.org/downloads/macos/), then reopen Terminal.
- **Linux:** install Python 3.11 or later and its virtual-environment support using your distribution's documented package manager. Package names and available versions vary. On Debian/Ubuntu, the relevant packages are commonly `python3` and `python3-venv`; check the resulting version before continuing. If your distribution supplies an older Python, obtain a supported newer interpreter using its documented instructions.

Run `python3 --version` again. If your suitable interpreter has a versioned name such as `python3.12`, use that name in step 3. Keep the operating system's Python installation intact.

## 2. Get the Notella source

Open the [Notella repository](https://github.com/mikevan/Notella) in your browser. Sign in if access is required, choose **Code → Download ZIP**, and extract the archive with your file manager. If you cannot access it, obtain access or a source ZIP from the project maintainer before continuing.

Create a folder named `Notella` inside your home folder and place the extracted project contents there. It should directly contain `docs`, `examples`, `notella`, `tests`, and `pyproject.toml`, without an extra nested `Notella-main` directory.

```sh
cd "$HOME/Notella"
ls
```

Confirm that those files and folders appear. If you chose another location, use its full path in quotes instead. This is the **project root**: run the tutorial commands here.

## 3. Create a separate Python environment

```sh
python3 -m venv .venv
./.venv/bin/python --version
./.venv/bin/python -c 'import sys; print(sys.executable)'
```

The last command should print a path inside `Notella/.venv/bin`. This environment keeps project packages separate; see Python's [virtual environment documentation](https://docs.python.org/3/library/venv.html). If Linux reports that `venv` or `ensurepip` is unavailable, install the virtual-environment package matching your interpreter and retry.

No activation is required when using this explicit interpreter path. The core runs from the project root without a package installation or dependency download.

## 4. Check the environment and run the example

Run each command separately and stop on an error:

```sh
./.venv/bin/python -m unittest discover -s tests -v
./.venv/bin/python -m examples.tutorial --store runtime/tutorial
```

The tests should finish with `OK`. The example should print four artifact IDs, splits of `train: 3`, `validation: 1`, `test: 1`, and:

```json
{
  "fixtureOnly": true,
  "modelLoaded": false,
  "trainingStarted": false,
  "semanticAccuracyMeasured": false
}
```

Read the saved result:

```sh
cat runtime/tutorial/tutorial-result.json
```

Notella creates the output folder automatically. This checks the local curriculum workflow, not model training or model accuracy.

## 5. Continue with Tutorial 1

Open [Tutorial 1](tutorial.md). Replace its `python` command with `./.venv/bin/python`. You have already completed its environment check and full example. Its later Python code is the same on every platform.

Use a plain-text editor to create `tutorial_walkthrough.py` in the project root. Paste the Python snippets into it in their displayed order, save, and run:

```sh
./.venv/bin/python tutorial_walkthrough.py
```

In TextEdit on macOS, choose **Format → Make Plain Text** before saving and ensure the file ends in `.py`, not `.txt`. Terminal commands belong in Terminal; Python snippets belong in the script. Keep the snippets together because they share variables.

When returning later, open Terminal, change to the project root again, and use the same `.venv` interpreter. You do not need to recreate it. Other guides currently show PowerShell examples; their environment-variable and HTTP commands need shell-specific equivalents on macOS/Linux.

## If a check fails

- **No module named `notella` or `examples`:** run from the directory containing both folders.
- **Permission denied while saving:** choose a folder owned by your user account. Do not run the tutorials with `sudo`.
- **Python is older than 3.11:** recreate the project environment with a suitable interpreter before continuing.
- **A test fails:** preserve the error output and resolve it before proceeding. See [troubleshooting](troubleshooting.md). These instructions do not claim that every operating system has been tested.

---

[Previous: Tutorial 0 — choose your environment](setup.md) · [Next: Tutorial 1 — your first semantic curriculum](tutorial.md)
