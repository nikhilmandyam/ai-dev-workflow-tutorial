import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

from pathlib import Path
from sales_data import load_sales

try:
    sales = load_sales(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except ValueError as exc:
    st.error(f"Unable to load sales data: {exc}")
    st.stop()

kpi_columns = st.columns(2)
st.subheader("Monthly Sales")
breakdown_columns = st.columns(2)
with breakdown_columns[0]:
    st.subheader("Sales by Category")
with breakdown_columns[1]:
    st.subheader("Sales by Region")
