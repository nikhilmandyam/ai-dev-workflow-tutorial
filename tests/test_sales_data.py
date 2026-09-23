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
