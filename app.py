from decimal import Decimal
from pathlib import Path

import plotly.express as px
import streamlit as st

from sales_data import calculate_kpis, category_sales, load_sales, monthly_sales, region_sales

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    sales = load_sales(Path(__file__).resolve().parent / "data" / "sales-data.csv")
except ValueError as exc:
    st.error(f"Unable to load sales data: {exc}")
    st.stop()

st.caption(f"Sales period: {sales['date'].min():%b %d, %Y} – {sales['date'].max():%b %d, %Y}")

kpi_columns = st.columns(2)
total_cents, order_count = calculate_kpis(sales)
kpi_columns[0].metric("Total Sales", f"${Decimal(total_cents) / 100:,.0f}")
kpi_columns[1].metric("Total Orders", f"{order_count:,}")
st.subheader("Monthly Sales")
trend = monthly_sales(sales)
trend["sales"] = trend["total_cents"].map(lambda cents: cents / 100)
figure = px.line(trend, x="month", y="sales", markers=True,
                 labels={"month": "Month", "sales": "Sales"},
                 color_discrete_sequence=["#2563EB"])
figure.update_xaxes(tickformat="%b %Y", dtick="M1")
figure.update_yaxes(tickprefix="$", tickformat=",.0f", rangemode="tozero")
figure.update_traces(hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.2f}<extra></extra>")
st.plotly_chart(figure, width="stretch")
breakdown_columns = st.columns(2)
for container, data, column, title in [
    (breakdown_columns[0], category_sales(sales), "category", "Sales by Category"),
    (breakdown_columns[1], region_sales(sales), "region", "Sales by Region"),
]:
    with container:
        st.subheader(title)
        data["sales"] = data["total_cents"].map(lambda cents: cents / 100)
        figure = px.bar(data, x="sales", y=column, orientation="h",
                        labels={"sales": "Sales", column: column.title()},
                        color_discrete_sequence=["#2563EB"])
        figure.update_yaxes(categoryorder="array", categoryarray=data[column].tolist(),
                            autorange="reversed")
        figure.update_xaxes(tickprefix="$", tickformat=",.0f")
        figure.update_traces(hovertemplate="%{y}<br>Sales: $%{x:,.2f}<extra></extra>")
        st.plotly_chart(figure, width="stretch")
