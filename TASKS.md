# Dashboard Tasks

This file tracks all work for the e-commerce analytics dashboard.

## Definition of Done

Before any milestone moves to Done:

- All milestone acceptance criteria are met.
- The app runs locally with `streamlit run app.py`.
- Changes are committed with the milestone ID in the commit message.

## To Do

## In Progress

## Done

### TASK-7: Streamlit Community Cloud deployment

Deploy the completed dashboard for stakeholder review through a public URL.

Live dashboard: [ShopSmart Sales Dashboard](https://ai-dev-workflow-tutorial-e6wnb7ajwv9rrs3uaufzu8.streamlit.app)

- [x] The app, dependencies, and CSV are configured for successful deployment to Streamlit Community Cloud.
- [x] A public, shareable URL is documented and opens the working dashboard without errors.
- [x] Deployed KPIs and all three charts match the locally verified dashboard.

Readiness: Step 8 prepared on Python 3.14.7; all four deployment inputs are
tracked, dependency installation/check passes, and 39 tests pass. Deployment
instructions are in `README.md`; evidence and review status are in
[the verification document](docs/sales-dashboard-verification.md#task-7-deployment-readiness--plan-step-8).
Final review found no actionable defects; the feature was merged into `main`
with merge commit `6fb4828` and pushed to GitHub. The user reported the live
deployment and accepted TASK-7 on September 23, 2026, explicitly requesting all
criteria checked and movement to Done. Deployment acceptance is user-reported;
the agent has not independently verified the cloud dashboard.

Commit:

Notes: clean

### TASK-6: Testing and refinement

Verify dashboard accuracy, performance, browser compatibility, and presentation quality.

Automated verification: 39 tests pass; dependency check passes; independent CSV
calculations match all KPI and grouped totals. Local app runs at
http://127.0.0.1:8506. The user confirmed correct KPIs and charts, readable
layout, no visible errors, and passing required browser and reload checks.
Evidence and manual checklist: [verification document](docs/sales-dashboard-verification.md).

- [x] All KPI and chart calculations are verified against the CSV, and the dashboard runs without errors or warnings.
- [x] The dashboard loads within 5 seconds and charts render within 2 seconds of data loading.
- [x] The dashboard works in Chrome, Firefox, Safari, and Edge, with clear labels and a professional appearance suitable for executive presentations.

Commit:

Notes: clean

### TASK-5: Category and region breakdowns

Show interactive bar charts comparing sales by product category and geographic region.

- [x] The category chart includes all five categories and sorts sales from highest to lowest.
- [x] The region chart includes North, South, East, and West and sorts sales from highest to lowest.
- [x] Both charts have clear labels, tooltips with exact values, and totals matching CSV aggregations.

Verification: 35 pytest tests pass, including new labels and alphabetical ties.
Independent CSV calculations match every category and region total; both sum to
11,650,021 cents ($116,500.21). AppTest confirms three charts, descending bar
ordering, labeled axes, and cent-precision hover templates, with no app exceptions,
errors, or warnings. The user confirmed five category bars and four region bars,
largest values at the top, a readable side-by-side layout, exact-cent hover
values, and no visible errors at http://127.0.0.1:8505.

Commit: bba947d

Notes: clean

### TASK-4: Sales trend chart

Show sales over time in an interactive line chart.

- [x] Sales are aggregated by day or month and plotted in chronological order across the dataset's date range.
- [x] The chart has clear time and sales axis labels and tooltips showing exact values.
- [x] Chart totals match the corresponding CSV aggregations.

Verification: 33 pytest tests pass, including chronological grouping across a
missing month and year boundary. All 12 monthly totals match independent CSV
calculations and reconcile to 11,650,021 cents ($116,500.21). AppTest confirms
one chart with labeled axes and a cent-precision hover template, with no app
exceptions, errors, or warnings. The user confirmed January through December
in chronological order, readable axes, exact-cent hover values, and no visible
errors at http://127.0.0.1:8504.

Commit: 7fc0bae

Notes: clean

### TASK-3: KPI cards

Display Total Sales and Total Orders prominently using the CSV data.

- [x] Total Sales equals the sum of `total_amount`, and Total Orders equals the transaction count.
- [x] Currency uses a dollar sign and thousands separators, and order counts use thousands separators where appropriate.
- [x] Sample-data KPIs show 482 orders and approximately $116,500 in sales, with exact values verified against the CSV.

Verification: 32 pytest tests pass. Independent CSV verification totals
$116,500.21 across 482 transactions; AppTest confirms Total Sales `$116,500`
and Total Orders `482`, with no app exceptions, errors, or warnings.
Streamlit starts locally at http://127.0.0.1:8503. The user confirmed
Total Sales `$116,500` and Total Orders `482` with no visible errors.

Commit: db7341b

Notes: clean

### TASK-2: Data loading and basic structure

Load the sales CSV and establish the dashboard layout and data-processing structure.

- [x] `data/sales-data.csv` loads all 482 transactions with the required columns and appropriate date, numeric, and categorical types.
- [x] Data loading and aggregation are organized into readable, reusable functions.
- [x] The layout provides KPI cards, a sales trend area, and side-by-side category and region chart areas.

Verification: 31 pytest tests pass; all 482 transactions load with parsed dates,
integer quantities, categorical strings, and exact integer cents. Streamlit starts
locally, and AppTest confirms the date caption and layout without app errors.
KPI/chart areas are placeholders for TASK-3–5; aggregation implementations belong
to those milestones. The user confirmed the correct sales-period caption, Monthly
Sales section, and side-by-side category and region areas, with no visible errors.

Commit: faf2add

Notes: clean

### TASK-1: Environment setup and project initialization

Set up the Python environment and a runnable Streamlit project.

- [x] Python 3.11+ setup instructions and dependencies for Streamlit, Pandas, and Plotly are provided.
- [x] A minimal `app.py` launches successfully and displays the dashboard title.

Verification: Local server startup and Streamlit AppTest passed on Python 3.14.7.
The user confirmed the dashboard title rendered at the local Streamlit URL with no visible errors.

Commit: c9a1348

Notes: clean
