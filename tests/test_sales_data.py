import csv
from pathlib import Path

import pytest

from sales_data import calculate_kpis, load_sales

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


def test_large_money_preserves_every_cent(tmp_path):
    amount = '1234567890123456789012345678.91'
    frame = load_sales(write_csv(tmp_path, [
        row(quantity='1', unit_price=amount, total_amount=amount),
    ]))
    assert frame.loc[0, 'total_cents'] == 123456789012345678901234567891


def test_kpis_preserve_cents(tmp_path):
    frame = load_sales(write_csv(tmp_path, [
        row(), row(order_id="B", quantity="1", unit_price="0.10", total_amount="0.10")
    ]))
    assert calculate_kpis(frame) == (30, 2)
