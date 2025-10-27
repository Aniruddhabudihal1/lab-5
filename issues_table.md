# Identified Issues and Fixes

| Issue Type | Tool | Location (original) | Description | Fix Approach |
|---|---|---:|---|---|
| Mutable default argument | Pylint | `addItem` (original) | `logs=[]` used as default, shared across calls causing state leakage | Changed signature to `add_item(item=None, qty=0)` and removed mutable default; use logging instead of appending to list |
| Bare except | Pylint/Bandit | `removeItem` (original) | `except:` swallowed all exceptions, hiding errors | Replaced with explicit validation and only catch specific exceptions where needed; return False on invalid input |
| Insecure eval usage | Bandit | `eval(...)` in `main` (original) | `eval` executes arbitrary code, high risk | Removed `eval` call entirely; used logging/prints for demonstration |
| File I/O without context/encoding | Flake8/Pylint | `loadData` / `saveData` (original) | Used `open()` without context manager and without encoding, risking resource leaks and encoding issues | Rewrote to use `with open(..., encoding='utf-8')` and handled FileNotFoundError / JSONDecodeError |
| Missing input validation / type errors | Pylint/Flake8 | `addItem(123, "ten")` and negative qty usage (original) | Functions accepted non-str item and non-int qty, allowing invalid state | Added type checks and conversions; return False for invalid inputs; enforce qty > 0 |
| Overly broad exception catch | Pylint | `saveData` (original) | Caught generic Exception which hides underlying errors | Catch OSError only when writing file and log exception |

Notes:
- After fixes, Pylint score is 10.00/10 and Bandit reports no issues. Flake8 returns no errors.
- I focused on medium/high severity issues first (mutable defaults, bare excepts, eval), then on style and robustness (naming, docstrings, encoding).
