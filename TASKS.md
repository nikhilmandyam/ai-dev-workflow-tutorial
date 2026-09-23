# Dashboard Tasks

This file tracks all work for the e-commerce analytics dashboard.

## Definition of Done

Before any milestone moves to Done:

- All milestone acceptance criteria are met.
- The app runs locally with `streamlit run app.py`.
- Changes are committed with the milestone ID in the commit message.

## To Do

### TASK-3: KPI cards

Display Total Sales and Total Orders prominently using the CSV data.

- [ ] Total Sales equals the sum of `total_amount`, and Total Orders equals the transaction count.
- [ ] Currency uses a dollar sign and thousands separators, and order counts use thousands separators where appropriate.
- [ ] Sample-data KPIs show 482 orders and approximately $116,500 in sales, with exact values verified against the CSV.

Commit:

### TASK-4: Sales trend chart

Show sales over time in an interactive line chart.

- [ ] Sales are aggregated by day or month and plotted in chronological order across the dataset's date range.
- [ ] The chart has clear time and sales axis labels and tooltips showing exact values.
- [ ] Chart totals match the corresponding CSV aggregations.

Commit:

### TASK-5: Category and region breakdowns

Show interactive bar charts comparing sales by product category and geographic region.

- [ ] The category chart includes all five categories and sorts sales from highest to lowest.
- [ ] The region chart includes North, South, East, and West and sorts sales from highest to lowest.
- [ ] Both charts have clear labels, tooltips with exact values, and totals matching CSV aggregations.

Commit:

### TASK-6: Testing and refinement

Verify dashboard accuracy, performance, browser compatibility, and presentation quality.

- [ ] All KPI and chart calculations are verified against the CSV, and the dashboard runs without errors or warnings.
- [ ] The dashboard loads within 5 seconds and charts render within 2 seconds of data loading.
- [ ] The dashboard works in Chrome, Firefox, Safari, and Edge, with clear labels and a professional appearance suitable for executive presentations.

Commit:

### TASK-7: Streamlit Community Cloud deployment

Deploy the completed dashboard for stakeholder review through a public URL.

- [ ] The app, dependencies, and CSV are configured for successful deployment to Streamlit Community Cloud.
- [ ] A public, shareable URL is documented and opens the working dashboard without errors.
- [ ] Deployed KPIs and all three charts match the locally verified dashboard.

Commit:

## In Progress

### TASK-2: Data loading and basic structure

Load the sales CSV and establish the dashboard layout and data-processing structure.

- [x] `data/sales-data.csv` loads all 482 transactions with the required columns and appropriate date, numeric, and categorical types.
- [x] Data loading and aggregation are organized into readable, reusable functions.
- [ ] The layout provides KPI cards, a sales trend area, and side-by-side category and region chart areas.

Verification: 31 pytest tests pass; all 482 transactions load with parsed dates,
integer quantities, categorical strings, and exact integer cents. Streamlit starts
locally, and AppTest confirms the date caption and layout without app errors.
KPI/chart areas are placeholders for TASK-3–5; aggregation implementations belong
to those milestones. Browser inspection remains pending because browser control
is unavailable in this session; TASK-2 stays In Progress until the layout is viewed.

Commit:

## Done

### TASK-1: Environment setup and project initialization

Set up the Python environment and a runnable Streamlit project.

- [x] Python 3.11+ setup instructions and dependencies for Streamlit, Pandas, and Plotly are provided.
- [x] A minimal `app.py` launches successfully and displays the dashboard title.

Verification: Local server startup and Streamlit AppTest passed on Python 3.14.7.
The user confirmed the dashboard title rendered at the local Streamlit URL with no visible errors.

Commit: c9a1348

Notes: clean
