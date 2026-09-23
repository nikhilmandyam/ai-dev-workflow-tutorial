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
