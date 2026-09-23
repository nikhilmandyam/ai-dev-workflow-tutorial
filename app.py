from pathlib import Path

import streamlit as st

from sales_data import load_sales

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    sales = load_sales(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except ValueError as exc:
    st.error(f"Unable to load sales data: {exc}")
    st.stop()

st.caption(f"Sales period: {sales['date'].min():%b %d, %Y} – {sales['date'].max():%b %d, %Y}")

kpi_columns = st.columns(2)
st.subheader("Monthly Sales")
breakdown_columns = st.columns(2)
with breakdown_columns[0]:
    st.subheader("Sales by Category")
with breakdown_columns[1]:
    st.subheader("Sales by Region")
