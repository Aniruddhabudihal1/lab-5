# Reflection

1. Which issues were the easiest to fix, and which were the hardest? Why?

- Easiest: Removing `eval` and replacing bare excepts were straightforward changes once identified. They involved simple code removals or replacing broad handlers with explicit checks.
- Hardest: Improving error handling around file I/O and deciding how to handle loading malformed JSON required careful thought to avoid data loss and keep predictable behavior.

2. Did the static analysis tools report any false positives? If so, describe one example.

- Not really false positives in this run. Some style hints (naming conventions) are suggestions and not strictly bugs; I converted names to snake_case to satisfy Pylint even though the original API could have kept the previous names for backward compatibility.

3. How would you integrate static analysis tools into your development workflow?

- Add Flake8 and Pylint checks as pre-commit hooks (via pre-commit) to catch style and obvious issues locally before commits.
- Run Bandit during CI (e.g., a GitHub Actions job) to catch security issues on every PR.
- Use a staged CI pipeline: quick lints (flake8) on push, deeper analysis (pylint, bandit) as required for merges.

4. Tangible improvements observed after applying fixes

- Code is more robust: functions validate inputs, avoiding runtime KeyError and TypeError.
- Security improved: `eval` removed and file reads/writes use safe context managers.
- Readability improved: consistent snake_case naming, docstrings added, and logging standardized.
- Static analysis reports now show no security issues and a perfect Pylint score, which increases confidence in maintainability.


---

Files added/updated as deliverables:
- `inventory_system.py` — cleaned and updated implementation.
- `issues_table.md` — documented the issues found and fixes.
- `reflection.md` — answers to lab reflection questions.
