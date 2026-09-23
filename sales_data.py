import csv
import re
from datetime import datetime
from decimal import Decimal, localcontext
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
    return validate_sales(pd.DataFrame(rows))


def money_cents(value: str, column: str, row_number: int) -> int:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", value):
        raise ValueError(f"CSV row {row_number}, {column}: expected nonnegative money with at most two decimals")
    # Preserve all input digits even beyond Decimal's default precision.
    with localcontext() as context:
        context.prec = len(value) + 2
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


def calculate_kpis(sales: pd.DataFrame) -> tuple[int, int]:
    return sum(sales["total_cents"]), len(sales)


def monthly_sales(sales: pd.DataFrame) -> pd.DataFrame:
    """Sum exact cents by month, including zero-sales gaps."""
    months = sales["date"].dt.to_period("M")
    totals = sales.groupby(months)["total_cents"].sum()
    complete_range = pd.period_range(months.min(), months.max(), freq="M")
    totals = totals.reindex(complete_range, fill_value=0)
    return pd.DataFrame({"month": complete_range.to_timestamp(),
                         "total_cents": totals.tolist()})


def _sales_by(sales: pd.DataFrame, column: str) -> pd.DataFrame:
    return (sales.groupby(column, as_index=False)["total_cents"].sum()
            .sort_values(["total_cents", column], ascending=[False, True])
            .reset_index(drop=True))


def category_sales(sales: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(sales, "category")


def region_sales(sales: pd.DataFrame) -> pd.DataFrame:
    return _sales_by(sales, "region")
