# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task, after the user reviews the plan and chooses an execution method. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the approved CSV-backed dashboard with accurate KPIs, monthly trends, category and region charts, and a final deployment handoff to the user.

**Architecture:** `sales_data.py` owns CSV loading, validation, and exact-cent calculations. `app.py` owns Streamlit layout, error presentation, and Plotly charts. Pytest exercises data behavior independently of the UI.

**Tech Stack:** Python 3.11+, standard-library venv and pip, Streamlit, Pandas, Plotly, pytest.

**Spec:** [Approved design](../specs/2026-09-22-sales-dashboard-design.md), approved by the user on September 22, 2026. Read it alongside `prd/ecommerce-analytics.md` and `TASKS.md`.

## Global Constraints

- Work on the current `feature/sales-dashboard` branch without creating a worktree.
- Use Python 3.11+, a plain virtual environment in `venv/`, and `requirements.txt` containing Streamlit, Pandas, Plotly, and pytest. Use pip; do not use uv or conda.
- Keep production code in two readable modules: `app.py` and `sales_data.py`.
- Keep calculations independent of the UI and test them with pytest.
- Show monthly trend totals, whole dollars on KPI cards and chart axes, and cents in tooltips. Display rounding must not change calculated totals.
- Stop with a clear error when data is missing or invalid; do not silently skip transactions.
- Deployment belongs to the user, from `main` after merge.
- Do not add filters, authentication, caching, background refresh, exports, or a database.

## Tracking and execution boundaries

**Step numbers are plan identifiers; TASK IDs are milestone identifiers.** Steps 2 and 3 both belong to TASK-2; Steps 8 and 9 both belong to TASK-7. Every checklist item inherits its heading's milestone.

At the start of work on a milestone, move it to In Progress in `TASKS.md`. Check acceptance criteria only after verification. Move it to Done only after all its criteria pass, the local app runs, and its implementation changes have a commit containing its TASK ID. Leave the board's `Commit:` lines blank for the user, as originally requested. Commit board updates separately if they follow the implementation commit. Do not mark milestones complete merely because a plan step is complete.

All commands below are future execution instructions, not commands to run while writing or reviewing this plan. Do not create a worktree, switch away from the feature branch, merge, push, or deploy as part of plan preparation. At implementation handoff, report the verified branch state and any remaining checks; merge happens through the user's review workflow before deployment.

## File map

| File | Change and responsibility |
| --- | --- |
| `app.py` | Create the page, data-error boundary, two KPI cards, and three charts. |
| `sales_data.py` | Create loader, validation helpers, and four aggregation functions. |
| `tests/test_sales_data.py` | Create CSV fixtures and validation/calculation tests. |
| `tests/test_app.py` | Create focused Streamlit smoke and error-boundary tests. |
| `requirements.txt` | Create dependency list; pin the four direct versions actually verified. |
| `README.md` | Append setup, launch, test, and deployment instructions; preserve tutorial content. |
| `docs/sales-dashboard-verification.md` | Record actual test, browser, timing, and deployment-readiness evidence. |
| `TASKS.md` | Update milestone states only as acceptance evidence permits. |
| `data/sales-data.csv` | Read without modifying the supplied data. |

`venv/` and pytest/Python caches are already ignored. No additional production modules are needed.

## Review Focus

- Nonfinite money and sub-cent amounts must fail instead of contaminating totals: Step 3 parameterized validation tests.
- A missing month across a year boundary must appear once with zero sales: Step 5 expected-series test.
- New category names and tied totals must remain visible with deterministic alphabetical ties: Step 6 fixture assertions.
- Launching outside the repository directory must still locate the CSV: Step 7 AppTest with a changed working directory.
- Missing or invalid CSV data must show an error without rendering partial metrics/charts: Step 7 patched-loader tests.

## Documentation references

Use [Streamlit chart rendering](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart) for `width="stretch"`, [AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest) for UI smoke tests, and [Plotly hover formatting](https://plotly.com/python/hover-text-and-formatting/) for explicit cent-precision tooltips. Deployment instructions follow [Streamlit Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy). Recheck compatibility with the versions installed during execution.

---

## Step 1 [TASK-1]: Create the environment and runnable page

**Files:** Create `requirements.txt`, `app.py`; append to `README.md`; update `TASKS.md`.

**Interfaces:** Produces a working Streamlit entrypoint; no data API yet.

- [x] Confirm `git branch --show-current` is `feature/sales-dashboard`, inspect `git status --short`, and preserve unrelated changes.
- [x] Verify `python3 --version` is at least 3.11, then create and activate the environment. If it is older, select an installed Python 3.11+ executable before creating the environment.

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

- [x] Create the initial dependency file with these four lines and install it:

```text
streamlit
pandas
plotly
pytest
```

```bash
python -m pip install -r requirements.txt
python -m pip check
```

- [x] Create the app shell:

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] Launch `streamlit run app.py`, verify the title in a browser, then stop the server. This shell requires a smoke check, not a test mirroring its literal title.
- [x] Append the preceding setup commands plus `streamlit run app.py` and `python -m pytest -q` to a dashboard section in `README.md`. Explain that the test command applies once tests exist.
- [x] Pin the installed direct dependency versions without dumping unrelated packages into the file:

```bash
python - <<'PY'
from importlib.metadata import version
from pathlib import Path
names = ("streamlit", "pandas", "plotly", "pytest")
Path("requirements.txt").write_text(
    "".join(f"{name}=={version(name)}\n" for name in names)
)
PY
```

- [x] Review the diff, update the milestone according to the tracking rules, and commit only relevant files with `TASK-1: Set up the Streamlit dashboard`.

## Step 2 [TASK-2]: Load structured CSV data

**Files:** Create `sales_data.py`, `tests/test_sales_data.py`; modify `app.py`.

**Interfaces:** `load_sales(path: str | Path) -> pd.DataFrame`. Step 2 returns required columns as strings; Step 3 completes validation and adds normalized numeric/date columns before calculations consume it.

- [x] Write reusable fixture data and structural tests first:

```python
import csv
from pathlib import Path

import pytest

from sales_data import load_sales

FIELDS = ["date", "order_id", "product", "category", "region",
          "quantity", "unit_price", "total_amount"]

def row(**changes):
    values = dict(zip(FIELDS, ["2024-01-03", "A", "Cable", "Audio",
                              "North", "2", "0.10", "0.20"]))
    return values | changes

def write_csv(tmp_path, rows, fields=FIELDS):
    path = tmp_path / "sales.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path

def test_loads_required_columns(tmp_path):
    frame = load_sales(write_csv(tmp_path, [row()]))
    assert len(frame) == 1
    assert set(FIELDS) <= set(frame.columns)

def test_missing_file(tmp_path):
    with pytest.raises(ValueError, match="Cannot read"):
        load_sales(tmp_path / "missing.csv")

def test_missing_column(tmp_path):
    fields = FIELDS[:-1]
    values = {key: value for key, value in row().items() if key in fields}
    with pytest.raises(ValueError, match="total_amount"):
        load_sales(write_csv(tmp_path, [values], fields))

def test_empty_data(tmp_path):
    with pytest.raises(ValueError, match="no transactions"):
        load_sales(write_csv(tmp_path, []))

@pytest.mark.parametrize("text", [
    "",
    ",".join(FIELDS) + '\n"unterminated',
    ",".join(FIELDS) + "\n2024-01-01,A\n",
    ",".join(FIELDS) + ",date\n",
])
def test_invalid_csv_structure(tmp_path, text):
    path = tmp_path / "bad.csv"
    path.write_text(text)
    with pytest.raises(ValueError):
        load_sales(path)
```

- [x] Run `python -m pytest tests/test_sales_data.py -q`. Confirm failure is due to the absent loader, not a broken test fixture.
- [x] Implement structural loading using standard CSV parsing so malformed row lengths and duplicate headers cannot silently shift columns:

```python
import csv
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["date", "order_id", "product", "category", "region",
                    "quantity", "unit_price", "total_amount"]

def load_sales(path: str | Path) -> pd.DataFrame:
    try:
        with Path(path).open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, strict=True)
            fields = reader.fieldnames or []
            missing = sorted(set(REQUIRED_COLUMNS) - set(fields))
            if missing:
                raise ValueError(f"Missing CSV columns: {', '.join(missing)}")
            if len(fields) != len(set(fields)):
                raise ValueError("CSV contains duplicate column names")
            rows = []
            for number, values in enumerate(reader, start=2):
                if None in values or any(value is None for value in values.values()):
                    raise ValueError(f"CSV row {number}: incorrect number of fields")
                rows.append({key: values[key].strip() for key in REQUIRED_COLUMNS})
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ValueError(f"Cannot read sales CSV: {exc}") from exc
    if not rows:
        raise ValueError("Sales CSV contains no transactions")
    return pd.DataFrame(rows)
```

- [x] In `app.py`, add the loader call after the title and before any metrics/charts. This boundary remains throughout the plan:

```python
from pathlib import Path
from sales_data import load_sales

try:
    sales = load_sales(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except ValueError as exc:
    st.error(f"Unable to load sales data: {exc}")
    st.stop()

kpi_columns = st.columns(2)
st.subheader("Monthly Sales")
breakdown_columns = st.columns(2)
with breakdown_columns[0]:
    st.subheader("Sales by Category")
with breakdown_columns[1]:
    st.subheader("Sales by Region")
```

- [ ] Run the loader tests, launch the app, inspect the basic structure, and commit `TASK-2: Load the sales CSV and establish page structure`. Keep TASK-2 In Progress until Step 3 passes.

## Step 3 [TASK-2]: Validate transactions and normalize exact cents

**Files:** Modify `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** `load_sales` now returns parsed dates, integer quantities, original monetary strings, and Python-integer `unit_price_cents` and `total_cents` columns. Internal `validate_sales(frame: pd.DataFrame) -> pd.DataFrame` raises `ValueError` for expected invalid data. Aggregation functions accept only this validated, nonempty frame.

- [x] Add failing tests for normalized values and invalid fields:

```python
def test_exact_cents_and_types(tmp_path):
    frame = load_sales(write_csv(tmp_path, [row()]))
    assert frame.loc[0, "total_cents"] == 20
    assert frame.loc[0, "unit_price_cents"] == 10
    assert frame.loc[0, "quantity"] == 2
    assert frame.loc[0, "date"].strftime("%Y-%m-%d") == "2024-01-03"

@pytest.mark.parametrize("column,value", [
    ("date", "2024-02-30"), ("date", "2024-1-3"),
    ("order_id", " "), ("product", ""), ("category", " "), ("region", ""),
    ("quantity", "0"), ("quantity", "-1"), ("quantity", "1.5"),
    ("quantity", "nan"), ("unit_price", "NaN"),
    ("unit_price", "Infinity"), ("unit_price", "-1.00"),
    ("unit_price", "0.001"), ("total_amount", "inf"),
    ("total_amount", "-0.20"), ("total_amount", "0.201"),
    ("total_amount", "0.21"), ("total_amount", ""),
])
def test_rejects_invalid_values(tmp_path, column, value):
    with pytest.raises(ValueError, match=column):
        load_sales(write_csv(tmp_path, [row(**{column: value})]))

def test_duplicate_order_id(tmp_path):
    with pytest.raises(ValueError, match="order_id"):
        load_sales(write_csv(tmp_path, [row(), row()]))

def test_zero_price_and_extra_column_are_allowed(tmp_path):
    values = row(unit_price="0.00", total_amount="0.00") | {"note": "promotion"}
    frame = load_sales(write_csv(tmp_path, [values], FIELDS + ["note"]))
    assert frame.loc[0, "total_cents"] == 0
```

- [x] Run `python -m pytest tests/test_sales_data.py -q` and confirm the new validation tests fail. Then add validation helpers and replace the loader's final return with `return validate_sales(pd.DataFrame(rows))`:

```python
import re
from datetime import datetime
from decimal import Decimal

def money_cents(value: str, column: str, row_number: int) -> int:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", value):
        raise ValueError(f"CSV row {row_number}, {column}: expected nonnegative money with at most two decimals")
    return int(Decimal(value) * 100)

def validate_sales(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    dates, quantities, prices, totals = [], [], [], []
    seen = set()
    for number, values in enumerate(frame.to_dict("records"), start=2):
        for column in REQUIRED_COLUMNS:
            if not values[column]:
                raise ValueError(f"CSV row {number}, {column}: value is required")
        if values["order_id"] in seen:
            raise ValueError(f"CSV row {number}, order_id: duplicate identifier")
        seen.add(values["order_id"])
        date_text = values["date"]
        try:
            if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date_text):
                raise ValueError("wrong format")
            date = datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(f"CSV row {number}, date: expected a valid YYYY-MM-DD date") from exc
        if not re.fullmatch(r"[0-9]+", values["quantity"]) or int(values["quantity"]) <= 0:
            raise ValueError(f"CSV row {number}, quantity: expected a positive integer")
        quantity = int(values["quantity"])
        price = money_cents(values["unit_price"], "unit_price", number)
        total = money_cents(values["total_amount"], "total_amount", number)
        if total != quantity * price:
            raise ValueError(f"CSV row {number}, total_amount: does not equal quantity times unit_price")
        dates.append(date)
        quantities.append(quantity)
        prices.append(price)
        totals.append(total)
    frame["date"] = pd.to_datetime(dates)
    frame["quantity"] = quantities
    frame["unit_price_cents"] = pd.Series(prices, dtype=object)
    frame["total_cents"] = pd.Series(totals, dtype=object)
    return frame
```

- [x] Add the date-range caption after successful loading and before the layout:

```python
st.caption(f"Sales period: {sales['date'].min():%b %d, %Y} – {sales['date'].max():%b %d, %Y}")
```

- [ ] Run the data tests and load the real CSV. Verify 482 rows load successfully, then launch the app. Do not alter the CSV to make tests pass. Update TASK-2 only after all its criteria pass, and commit `TASK-2: Validate transactions and preserve exact cents`.

## Step 4 [TASK-3]: Calculate and display the KPIs

**Files:** Modify `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** `calculate_kpis(sales: pd.DataFrame) -> tuple[int, int]` returns `(total_cents, transaction_count)`.

- [x] Add and run this failing test with `python -m pytest tests/test_sales_data.py -k kpis -q`:

```python
from sales_data import calculate_kpis

def test_kpis_preserve_cents(tmp_path):
    frame = load_sales(write_csv(tmp_path, [
        row(), row(order_id="B", quantity="1", unit_price="0.10", total_amount="0.10")
    ]))
    assert calculate_kpis(frame) == (30, 2)
```

- [x] Implement the calculation:

```python
def calculate_kpis(sales: pd.DataFrame) -> tuple[int, int]:
    return sum(sales["total_cents"]), len(sales)
```

- [x] Import `calculate_kpis` into `app.py` and fill the existing KPI columns. Use Decimal for the display conversion, leaving the stored total unchanged:

```python
from decimal import Decimal

total_cents, order_count = calculate_kpis(sales)
kpi_columns[0].metric("Total Sales", f"${Decimal(total_cents) / 100:,.0f}")
kpi_columns[1].metric("Total Orders", f"{order_count:,}")
```

- [ ] Run all data tests, then launch locally and verify `$116,500` and `482`. Update TASK-3 and commit `TASK-3: Display exact sales and order KPIs`.

## Step 5 [TASK-4]: Aggregate and chart monthly sales

**Files:** Modify `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** `monthly_sales(sales: pd.DataFrame) -> pd.DataFrame` returns `month` (month-start timestamp) and `total_cents` (integer), including zero-sales gaps.

- [ ] Add the failing test and run `python -m pytest tests/test_sales_data.py -k monthly -q`:

```python
from sales_data import monthly_sales

def test_monthly_sales_cross_year_gap_and_order(tmp_path):
    frame = load_sales(write_csv(tmp_path, [
        row(date="2025-02-03"),
        row(order_id="B", date="2024-12-12"),
        row(order_id="C", date="2024-12-01"),
    ]))
    result = monthly_sales(frame)
    assert result["month"].dt.strftime("%Y-%m").tolist() == ["2024-12", "2025-01", "2025-02"]
    assert result["total_cents"].tolist() == [40, 0, 20]
```

- [ ] Implement:

```python
def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    months = sales["date"].dt.to_period("M")
    totals = sales.groupby(months)["total_cents"].sum()
    complete_range = pd.period_range(months.min(), months.max(), freq="M")
    totals = totals.reindex(complete_range, fill_value=0)
    return pd.DataFrame({"month": complete_range.to_timestamp(),
                         "total_cents": totals.tolist()})
```

- [ ] Import `plotly.express as px` and `monthly_sales` in `app.py`. Insert the chart immediately after the Monthly Sales subheading, before creating breakdown columns:

```python
trend = monthly_sales(sales)
trend["sales"] = trend["total_cents"].map(lambda cents: cents / 100)
figure = px.line(trend, x="month", y="sales", markers=True,
                 labels={"month": "Month", "sales": "Sales"},
                 color_discrete_sequence=["#2563EB"])
figure.update_xaxes(tickformat="%b %Y", dtick="M1")
figure.update_yaxes(tickprefix="$", tickformat=",.0f", rangemode="tozero")
figure.update_traces(hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>")
st.plotly_chart(figure, width="stretch")
```

- [ ] Run all data tests and launch the app. Verify 12 chronological months, clearly labeled axes, cent-precision hover values, and reconciliation to 11,650,021 cents. Update TASK-4 and commit `TASK-4: Add monthly sales trend`.

## Step 6 [TASK-5]: Aggregate and chart category and region sales

**Files:** Modify `sales_data.py`, `tests/test_sales_data.py`, `app.py`, `TASKS.md`.

**Interfaces:** `category_sales(sales: pd.DataFrame) -> pd.DataFrame` returns `category, total_cents`; `region_sales(sales: pd.DataFrame) -> pd.DataFrame` returns `region, total_cents`. Both sort sales descending and labels ascending for ties.

- [ ] Add and run the failing breakdown tests:

```python
from sales_data import category_sales, region_sales

@pytest.mark.parametrize("function,column", [
    (category_sales, "category"), (region_sales, "region")
])
def test_breakdowns_sum_sort_and_include_new_labels(tmp_path, function, column):
    frame = load_sales(write_csv(tmp_path, [
        row(**{column: "Zeta"}),
        row(order_id="B", **{column: "Alpha"}),
        row(order_id="C", **{column: "New label"}),
        row(order_id="D", **{column: "New label"}),
    ]))
    result = function(frame)
    assert result[column].tolist() == ["New label", "Alpha", "Zeta"]
    assert result["total_cents"].tolist() == [40, 20, 20]
```

Run `python -m pytest tests/test_sales_data.py -k breakdowns -q`; expect failure before implementing the functions.

- [ ] Implement one small shared aggregation helper and two explicit public functions:

```python
def _sales_by(sales: pd.DataFrame, column: str) -> pd.DataFrame:
    return (sales.groupby(column, as_index=False)["total_cents"].sum()
            .sort_values(["total_cents", column], ascending=[False, True])
            .reset_index(drop=True))

def category_sales(sales: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(sales, "category")

def region_sales(sales: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(sales, "region")
```

- [ ] Import both functions in `app.py` and replace the two empty breakdown areas with this rendering loop. Keep it in `app.py`; no separate chart module:

```python
for container, data, column, title in [
    (breakdown_columns[0], category_sales(sales), "category", "Sales by Category"),
    (breakdown_columns[1], region_sales(sales), "region", "Sales by Region"),
]:
    with container:
        st.subheader(title)
        data["sales"] = data["total_cents"].map(lambda cents: cents / 100)
        figure = px.bar(data, x="sales", y=column, orientation="h",
                        labels={"sales": "Sales", column: column.title()},
                        color_discrete_sequence=["#2563EB"])
        figure.update_yaxes(categoryorder="array", categoryarray=data[column].tolist(),
                            autorange="reversed")
        figure.update_xaxes(tickprefix="$", tickformat=",.0f")
        figure.update_traces(hovertemplate="%{y}<br>Sales: $%{x:,.2f}<extra></extra>")
        st.plotly_chart(figure, width="stretch")
```

- [ ] Run all data tests and launch locally. Verify all five categories, all four regions, highest bars at the top, exact tooltips, and readable side-by-side charts. Update TASK-5 and commit `TASK-5: Add category and region breakdowns`.

## Step 7 [TASK-6]: Verify the assembled dashboard and refine it

**Files:** Modify `tests/test_sales_data.py`; create `tests/test_app.py`, `docs/sales-dashboard-verification.md`; modify `app.py` or `sales_data.py` only for demonstrated failures; update `TASKS.md`.

**Interfaces:** Consumes all four aggregation functions, `load_sales`, and the app entrypoint; produces verification evidence without new production APIs.

- [ ] Add the supplied-data regression test:

```python
def test_supplied_csv_totals_and_dimensions():
    path = Path(__file__).resolve().parents[1] / "data" / "sales-data.csv"
    frame = load_sales(path)
    assert calculate_kpis(frame) == (11650021, 482)
    assert set(category_sales(frame)["category"]) == {
        "Electronics", "Accessories", "Audio", "Wearables", "Smart Home"
    }
    assert set(region_sales(frame)["region"]) == {"North", "South", "East", "West"}
    assert category_sales(frame).iloc[0]["category"] == "Electronics"
    assert len(monthly_sales(frame)) == 12
    for summary in (monthly_sales(frame), category_sales(frame), region_sales(frame)):
        assert sum(summary["total_cents"]) == 11650021
```

- [ ] Create focused UI integration tests. These check visible behavior rather than internal chart serialization:

```python
from pathlib import Path
from unittest.mock import patch

import pytest
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"

def test_dashboard_from_another_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app = AppTest.from_file(str(APP)).run(timeout=15)
    assert not app.exception
    assert not app.error
    assert not app.warning
    assert [(metric.label, metric.value) for metric in app.metric] == [
        ("Total Sales", "$116,500"), ("Total Orders", "482")
    ]
    assert len(app.get("plotly_chart")) == 3

@pytest.mark.parametrize("message", [
    "Cannot read sales CSV: file missing",
    "CSV row 2, total_amount: invalid value",
])
def test_data_error_stops_rendering(message):
    with patch("sales_data.load_sales", side_effect=ValueError(message)):
        app = AppTest.from_file(str(APP)).run(timeout=15)
    assert not app.exception
    assert len(app.error) == 1
    assert message in app.error[0].value
    assert not app.metric
    assert len(app.get("plotly_chart")) == 0
```

- [ ] Run `python -m pytest -q` and `python -m pip check`. New integration tests may pass immediately because they verify already-built behavior. For any failure, isolate it with its test, fix only its cause, and rerun the affected tests followed by the complete suite.
- [ ] Run `streamlit run app.py`. Check the title, date range, whole-dollar formatting, hover cents, chart ordering, labels, and absence of runtime warnings/errors. Inspect actual tooltips; AppTest does not establish browser rendering quality.
- [ ] Check Chrome, Firefox, Safari, and Edge. Record browser versions, viewport, result, and any unavailable browser in `docs/sales-dashboard-verification.md`. An unavailable required browser remains an outstanding TASK-6 check.
- [ ] Measure local navigation-to-dashboard visibility and CSV-load-completion-to-all-charts-visible timing over three reloads with the server already running. Use temporary timing logs at loader completion plus a browser performance recording; remove diagnostic code afterward. Record machine, browser, dataset size, cache conditions, and all measurements. Each measured run must meet the five-second dashboard and two-second chart targets. Do not substitute HTTP response time or AppTest runtime for chart rendering time.
- [ ] Refine spacing and labeling only where visual inspection identifies a problem. After a code change, rerun relevant tests and the affected visual check; retain two production modules.
- [ ] Record actual commands, results, timing measurements, and unresolved checks in the verification document. Update TASK-6 only when all criteria pass, and commit `TASK-6: Verify dashboard accuracy and presentation`.

## Step 8 [TASK-7]: Prepare deployment documentation and hand off the branch

**Files:** Modify `README.md`, `docs/sales-dashboard-verification.md`, `TASKS.md`; adjust `requirements.txt` only if compatibility verification requires it.

**Interfaces:** Produces a reviewed, locally verified repository ready for the user's merge workflow and deployment. No deployment API or cloud resources are created.

- [ ] Confirm the tracked deployment inputs and environment health:

```bash
git ls-files app.py sales_data.py requirements.txt data/sales-data.csv
python -m pip install -r requirements.txt
python -m pip check
python -m pytest -q
git diff --check
```

Expected: all four application files are tracked, dependencies resolve, all tests pass, and the diff has no whitespace errors. Reuse Step 7 evidence unless changes justify repeating manual checks.

- [ ] Append these concrete deployment instructions to `README.md`: after review and merge, deploy the GitHub repository's `main` branch with entrypoint `app.py`; select the same supported Python minor version used for local verification; install from the root `requirements.txt`; make the app publicly accessible; verify both KPIs and all three charts; then record the actual public URL. No secrets are required for this CSV-backed app. Record the tested Python version now, not a guessed version.
- [ ] Record deployment-readiness evidence, outstanding checks, and the branch's review status in `docs/sales-dashboard-verification.md`. Check only TASK-7's deployment-configuration criterion if satisfied; leave public URL and deployed-parity criteria unchecked.
- [ ] Commit the readiness documentation with `TASK-7: Prepare deployment handoff`. Report the implementation commits and remaining user actions. Do not merge or deploy automatically; leave the branch ready for the user's review and merge workflow.

## Step 9 [TASK-7]: Deploy from main — Owner: user

**Final plan step. The agent stops at this handoff. The following checklist is for the user to execute after merge.**

**Files:** User records the resulting URL in `README.md` and completion evidence in `TASKS.md` and `docs/sales-dashboard-verification.md`.

**Prerequisite:** The reviewed feature has been merged into the remote `main` branch and required local acceptance checks pass. Do not deploy the feature branch.

- [ ] In Streamlit Community Cloud, create an app using this GitHub repository, branch `main`, and entrypoint `app.py`. Choose the locally verified Python minor version in advanced settings and deploy. Follow the linked official deployment instructions if the UI labels change.
- [ ] Verify public access in a signed-out/private browser window. Confirm Total Sales `$116,500`, Total Orders `482`, 12 monthly totals, five categories, four regions, correct rankings, exact cent tooltips, and no errors. Compare all three charts with the locally verified dashboard.
- [ ] Record the real shareable URL and verification outcome. Commit the documentation changes with `TASK-7: Record verified public deployment`; follow the repository's normal review workflow for those changes.
- [ ] Move TASK-7 to Done only after its acceptance criteria and the board's Definition of Done are satisfied, and fill its `Commit:` line with the relevant commit. Deployment failures keep TASK-7 In Progress.
