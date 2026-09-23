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
