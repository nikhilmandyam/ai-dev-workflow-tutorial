# Repository Guidelines

## Project Structure & Module Organization

This repository combines an AI-assisted development tutorial with a CSV-backed
Streamlit sales dashboard.

- `app.py`: page layout, KPI cards, Plotly charts, and user-facing error handling.
- `sales_data.py`: CSV loading, validation, and exact-cent aggregations; keep calculations independent of Streamlit.
- `tests/test_sales_data.py`: validation and calculation tests.
- `tests/test_app.py`: Streamlit AppTest integration and error-boundary tests.
- `data/sales-data.csv`: supplied transaction data; preserve it when changing code.
- `prd/` and `docs/superpowers/`: requirements, approved design, and implementation plan.
- `TASKS.md`: milestone board; `docs/sales-dashboard-verification.md`: verification evidence.

Preserve the tutorial content in `README.md` and the root-level workshop guides.

## Build, Test, and Development Commands

Use Python 3.11+ with a plain virtual environment and pip:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
streamlit run app.py
python -m pytest -q
git diff --check
```

These commands create the environment, install pinned dependencies, validate
compatibility, launch the dashboard, run the full suite, and check whitespace.
On Windows PowerShell, activate with `venv\Scripts\Activate.ps1`. No separate
build step or configured formatter/linter is required.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` functions and variables, and uppercase
constants. Follow existing Python style; prefer small functions and descriptive
names. Keep production code in `app.py` and `sales_data.py`. Calculate money in
integer cents; convert only for presentation. Invalid data must produce a clear
error and stop rendering rather than silently omit transactions.

## Testing Guidelines

Use pytest with `test_*.py` files and `test_*` functions. Add regression tests for
behavior changes, including invalid inputs and exact totals. Use AppTest for UI
integration; it does not prove browser rendering or performance. Run the full
suite before committing. No numeric coverage threshold is configured. Record
manual browser, tooltip, and timing evidence in the verification document.

## Commit & Pull Request Guidelines

Follow the history's milestone prefix: `TASK-6: Verify dashboard accuracy and presentation`.
Keep commits focused and update `TASKS.md` as acceptance evidence permits.
Pull requests should identify the milestone, describe behavior changes, report
test results, and include screenshots for visual changes. Review before merging.
Deployment is user-owned from `main` after merge; do not deploy automatically.

## Lessons

All completed milestones currently record `Notes: clean` in `TASKS.md`.

- Treat `clean` as no recorded corrective lesson; do not invent past issues.
- Record concrete lessons in milestone Notes when issues arise, and carry actionable rules into this section.
