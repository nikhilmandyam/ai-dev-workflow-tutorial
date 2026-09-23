# Sales dashboard verification

Recorded September 22, 2026 for TASK-6 / plan Step 7 on
`feature/sales-dashboard`, starting at `70c5090`.

**Status: TASK-6 accepted following user-reported manual verification.**
The user confirmed Total Sales `$116,500`, Total Orders `482`, correct monthly
and category/region charts, readable layout, no visible errors, and passing
required browser/reload checks. Automated checks also pass. No production code
or source CSV changes were needed.

Manual results below are the user's confirmation, not agent-observed browser
measurements. Exact browser versions, viewports, per-run durations, recording
files, and measurement conditions were not supplied and are not invented here.

## Environment and automated evidence

- Machine: macOS 26.6.2, arm64; Python 3.14.7 in `venv/`.
- Direct dependencies: Streamlit 1.64.0, Pandas 3.0.6, Plotly 7.1.0, pytest 9.1.1.
- Dataset: `data/sales-data.csv`, 32,167 bytes, 482 transactions,
  January 3–December 31, 2024.
- Execution: Native in this session; no subagents. Self-review found no code
  issues against Step 7 and the plan's Review Focus. Independent review has not
  been performed.

Commands run from the repository root:

| Command / check | Actual result |
| --- | --- |
| `venv/bin/python -m pytest -q` | 39 passed in 1.60s; no pytest warnings or failures |
| `venv/bin/python -m pip check` | No broken requirements; sandbox emitted a pip cache-directory warning |
| `venv/bin/python -m pip --no-cache-dir check` | No broken requirements; no cache warning |
| `git diff --check` | Passed, no whitespace errors |
| Independent standard-library `csv.DictReader` / `Decimal` calculation, compared to all four aggregation functions | Every group matched; total 11,650,021 cents and 482 transactions |
| `venv/bin/streamlit run app.py --server.address 127.0.0.1 --server.port 8506 --server.headless true --browser.gatherUsageStats false` | Server started at http://127.0.0.1:8506 after sandbox socket permission retry |

The server emitted an optional Watchdog installation suggestion. This is not a
dashboard warning or a measured performance failure. The user subsequently
confirmed the manual verification passed with no visible errors.

The new supplied-data regression checks exact KPIs, category/region membership,
Electronics ranking first, 12 months, and reconciliation of all summaries.
AppTest checks successful rendering from another working directory (two correct
metrics, three charts, no app exceptions/errors/warnings), and missing/invalid
data errors stopping before any metrics or charts appear. Existing tests cover
nonfinite/sub-cent money, invalid input, missing months across a year boundary,
and new labels with alphabetical ties. The new tests passed immediately because
they cover previously implemented behavior; no artificial production failure
was introduced.

Independent expected totals below were calculated from raw CSV strings using
`int(Decimal(row['total_amount']) * 100)` and standard-library dictionaries,
then compared with each production summary. Every summary totals $116,500.21.

| Month | Sales |
| --- | ---: |
| Jan 2024 | $7,175.17 |
| Feb 2024 | $8,426.07 |
| Mar 2024 | $9,603.10 |
| Apr 2024 | $9,021.03 |
| May 2024 | $8,406.95 |
| Jun 2024 | $9,600.93 |
| Jul 2024 | $9,474.93 |
| Aug 2024 | $9,993.97 |
| Sep 2024 | $9,159.99 |
| Oct 2024 | $9,649.89 |
| Nov 2024 | $10,801.84 |
| Dec 2024 | $15,186.34 |

| Category (top to bottom) | Sales |
| --- | ---: |
| Electronics | $42,683.67 |
| Wearables | $23,698.23 |
| Audio | $19,638.44 |
| Smart Home | $19,317.23 |
| Accessories | $11,162.64 |

| Region (top to bottom) | Sales |
| --- | ---: |
| North | $38,857.24 |
| West | $27,463.74 |
| East | $26,783.53 |
| South | $23,395.70 |

## Manual browser checklist — owner: user

The user confirmed the manual verification and required browser checks passed
at the local dashboard. The checklist records that overall acceptance.

- [x] Title reads “ShopSmart Sales Dashboard”; period is Jan 03, 2024 – Dec 31, 2024.
- [x] KPI cards show Total Sales `$116,500` and Total Orders `482`.
- [x] Monthly chart spans Jan–Dec 2024 chronologically; axes and labels are readable.
- [x] Five category bars and four region bars appear side by side, largest at top.
- [x] Revenue axes show whole dollars with separators; actual hovered tooltips
  show exact cents matching the tables above. Exercise all three charts.
- [x] No overlapping/clipped labels, unreadable text, or awkward spacing;
  appearance is suitable for executive presentations.
- [x] No visible app warnings/errors or browser console runtime errors.

| Browser | Version | Viewport / zoom | Result / issues |
| --- | --- | --- | --- |
| Chrome | Not supplied | Not supplied | Passed — user confirmation |
| Firefox | Not supplied | Not supplied | Passed — user confirmation |
| Safari | Not supplied | Not supplied | Passed — user confirmation |
| Edge | Not supplied | Not supplied | Passed — user confirmation |

## Manual performance evidence — owner: user

The user confirmed the required reload checks passed, accepting the five-second
dashboard and two-second chart targets across the required three reloads. Exact
durations and recordings were not supplied. Test runtime and HTTP response
time are not used as rendering evidence.

The original measurement procedure is retained below for reproducibility; its
specific instrumentation and conditions were not independently confirmed.

Use three reloads with the local server already running. Record machine/OS,
browser/version, viewport/zoom, dataset size, browser cache enabled/disabled,
reload type, network/CPU throttling, and any extensions affecting the run.
Use the same conditions across all three runs. There is no application caching.

For each run, capture a browser performance recording with screenshots, from
before reload until both lower charts have rendered. Use a viewport large enough
to see all three charts and record its dimensions. Temporarily add the following
immediately after the successful `sales = load_sales(...)` line in `app.py`,
inside its `try` block, to timestamp completion of loading and validation:

```python
    import time
    print(f"TASK6_CSV_LOAD_COMPLETE epoch_ns={time.time_ns()}", flush=True)
```

Save the server log and browser recording for each run. On this local machine,
correlate that wall-clock timestamp with the recording's navigation origin
(`performance.timeOrigin`, epoch milliseconds). Express all three events on the
same timeline: navigation start, CSV completion, and the screenshot frames where
the dashboard and all three charts are visible. Record timestamp alignment and
measurement precision; do not claim a pass if uncertainty crosses a limit.

| Run | Navigation → dashboard visible (≤5s) | CSV completion → all charts visible (≤2s) | Recording / log reference | Result |
| --- | --- | --- | --- | --- |
| 1 | Passed; exact duration not supplied | Passed; exact duration not supplied | Not supplied | User confirmation of required reload checks |
| 2 | Passed; exact duration not supplied | Passed; exact duration not supplied | Not supplied | User confirmation of required reload checks |
| 3 | Passed; exact duration not supplied | Passed; exact duration not supplied | Not supplied | User confirmation of required reload checks |

Measurement conditions and timestamp alignment: **Not supplied**.

Remove the temporary import/log line after recording. No diagnostic code has
been added at this handoff. Rerun the full suite and `git diff --check` after
removal or any refinement. If inspection reveals a presentation defect, fix
only that demonstrated issue and repeat its visual check and relevant tests.

## Acceptance and closeout

The user accepted TASK-6 and explicitly requested all acceptance criteria checked,
`Notes: clean`, movement to Done, and a commit and push on
`feature/sales-dashboard`. The commit message is
`TASK-6: Verify dashboard accuracy and presentation`. Its `Commit:` board field
remains reserved for the user. TASK-7 deployment is outside this work's scope.
