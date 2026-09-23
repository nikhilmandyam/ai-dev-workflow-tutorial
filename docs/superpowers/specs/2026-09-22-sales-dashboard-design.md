# E-commerce sales dashboard design

Status: Ready for user review. Implementation planning begins after approval.

## Purpose and scope

Build the Phase 1 dashboard in `prd/ecommerce-analytics.md` so ShopSmart stakeholders can understand sales performance at a glance. `TASKS.md` remains the milestone tracker.

The dashboard displays Total Sales, Total Orders, monthly sales trends, and sales by category and region using the repository's CSV. This release is a snapshot of that file, not a live data feed. Authentication, filters, exports, database integration, automated refresh, and transaction drill-down remain out of scope.

## Agreed constraints

- Work on the current `feature/sales-dashboard` branch without creating a worktree.
- Use Python 3.11+, a plain virtual environment in `venv/`, and `requirements.txt` containing Streamlit, Pandas, Plotly, and pytest. Use pip; do not use uv or conda.
- Keep production code in two readable modules: `app.py` and `sales_data.py`.
- Keep calculations independent of the UI and test them with pytest.
- Show monthly trend totals, whole dollars on KPI cards and chart axes, and cents in tooltips. Display rounding must not change calculated totals.
- Stop with a clear error when data is missing or invalid; do not silently skip transactions.
- Produce and review this design before creating an implementation plan.
- Deployment belongs to the user, from `main` after merge.

## Structure and responsibilities

| File | Responsibility |
| --- | --- |
| `app.py` | Resolve the CSV path relative to the application file, call the data functions, handle expected data errors, and render Streamlit metrics and Plotly charts. |
| `sales_data.py` | Load and validate the CSV, calculate KPIs, and return monthly, category, and region sales summaries. No Streamlit or Plotly imports. |
| `tests/test_sales_data.py` | Test validation and calculations with small fixtures and verify the supplied CSV. |
| `requirements.txt` | Declare the runtime and testing dependencies with versions verified during implementation. |
| `README.md` | Document environment setup, local launch, tests, and the user's deployment handoff. Preserve existing tutorial content. |
| `data/sales-data.csv` | Source transaction data. |

Use small functions with descriptive names and straightforward inputs and outputs. A loader returns a validated Pandas DataFrame; calculation functions accept that frame and return KPI values or aggregated DataFrames. Avoid classes, configuration frameworks, and extra abstraction layers.

## Data flow and validation

The application loads `data/sales-data.csv`, validates it, calculates summaries, and then renders the page. The dataset is small, so the initial design needs no caching or background processing.

The following validation rules are proposed as part of this design review:

- Require a readable, well-formed, nonempty CSV with all eight PRD columns. Extra columns may be ignored.
- Require nonblank values in all required columns and valid calendar dates in `YYYY-MM-DD` form.
- Require nonblank categorical strings and unique `order_id` values, consistent with the PRD's unique order identifier definition.
- Require positive integer quantities and finite, nonnegative monetary values with no more than two decimal places. Refunds are outside this dataset's defined transaction model.
- Require `total_amount` to equal `quantity * unit_price` at cent precision.

Read money as decimal strings, validate using Python's standard-library decimal support, and convert to integer cents for aggregation. Convert to dollar values only for presentation. This keeps financial totals exact while leaving Pandas grouping simple.

Do not hard-code the sample's row count, category names, regions, or date range into the loader. Those are sample-data checks, so a replacement CSV with the same schema can still work.

For expected file, parsing, or validation failures, the data module raises a clear exception. `app.py` shows an actionable error naming the problem and, where relevant, the column and CSV row, then stops before displaying KPIs or charts. It must not substitute zero values or partial results. Unexpected programming errors should remain visible during development.

## Calculation rules

- **Total Sales:** Sum `total_amount` in cents across all transactions.
- **Total Orders:** Count transaction rows, as specified in the PRD.
- **Monthly trend:** Sum sales by calendar month, retaining the year and sorting chronologically. Include months between the earliest and latest transaction months; a month with no transactions shows zero.
- **Category and region summaries:** Sum sales for every category or region present. Sort descending by sales, with alphabetical ordering for ties.

Read-only inspection of the supplied CSV confirmed 482 transactions, $116,500.21 in sales, dates from January 3 through December 31, 2024, five categories, four regions, and no duplicate order IDs. The revenue card therefore displays $116,500. Exact fixture and CSV assertions will use cents rather than the PRD's approximate revenue figure.

## Page layout and presentation

Use the title **ShopSmart Sales Dashboard**, following the company name in the PRD narrative. Beneath it, show the dataset's date range so viewers understand the period covered.

1. Two prominent KPI cards: Total Sales and Total Orders.
2. A full-width monthly sales line chart, labeled by month and year, with sales on the vertical axis.
3. Two horizontal bar charts side by side: Sales by Category and Sales by Region. The largest value appears at the top.

Use a wide page layout, consistent chart colors, readable labels, and minimal custom styling. Format revenue cards and chart axes as dollars with thousands separators and no cents; format order counts as integers with separators. Tooltips show the month, category, or region and its exact sales amount to two decimal places. No sidebar or filtering controls are needed.

## Verification strategy

Pytest will cover independently calculated fixture totals, transaction counts, chronological monthly grouping across year boundaries, zero-transaction months, category and region totals, descending sorting, and money precision. Validation tests will exercise missing files or columns, empty data, invalid dates, blank fields, duplicate IDs, invalid numeric values, and inconsistent transaction amounts.

Sample-data checks will confirm the 482 rows and 11,650,021 cents total, the five categories and four regions, and that each grouped summary reconciles to total sales. Tests should check behavior and expected results rather than copy the implementation's aggregation expressions.

Local verification includes `pytest` and `streamlit run app.py`, checking that the normal dashboard has no errors or warnings, tooltips and formatting work, and invalid data produces the expected clear error. Manual checks cover Chrome, Firefox, Safari, and Edge, professional appearance, dashboard load within five seconds, and charts rendering within two seconds of data loading. Record browser coverage and measured conditions; report any checks that cannot be performed rather than claiming they passed.

## Milestone coverage and planning contract

This table maps design scope to the existing milestones; it is not the implementation plan.

| Milestone | Scope covered by the later plan |
| --- | --- |
| TASK-1 | Python environment, dependencies, setup instructions, runnable app shell. |
| TASK-2 | CSV loading, validation, basic layout, and data-module tests. |
| TASK-3 | KPI calculations, tests, and formatted cards. |
| TASK-4 | Monthly aggregation, tests, and interactive trend chart. |
| TASK-5 | Category and region aggregations, tests, and sorted charts. |
| TASK-6 | Accuracy checks, error behavior, performance, browser checks, and presentation refinement. |
| TASK-7 | Deployment readiness and the final user-owned deployment handoff. |

The implementation plan will number its tasks independently as **Step 1**, **Step 2**, and so on, with every step labeled by its milestone, such as **Step 1 [TASK-1]**. All seven milestones must be covered. Milestones move to Done only when their acceptance criteria and the Definition of Done in `TASKS.md` are satisfied, including a working local app and commits containing the relevant milestone ID.

Deployment must be the final plan step, explicitly labeled **[TASK-7] — Owner: user**. After the feature is merged into `main`, the user deploys from `main` to Streamlit Community Cloud, verifies the public dashboard against local results, and records the shareable URL. The agent stops at that handoff; TASK-7 remains incomplete until the user performs and verifies deployment. There will be no agent-executed deployment or additional plan steps after the handoff.
