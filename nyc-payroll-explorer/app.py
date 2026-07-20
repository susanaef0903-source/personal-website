# ============================================
# NYC Payroll Explorer
# Analyzing New York City's public payroll data
# through the eyes of a 20-year payroll professional.
#
# Data: NYC Open Data — Citywide Payroll (Fiscal Year)
# https://data.cityofnewyork.us/City-Government/Citywide-Payroll-Data-Fiscal-Year-/k397-673e
#
# To run locally:  streamlit run app.py
# ============================================

import pandas as pd
import requests
import streamlit as st

API = "https://data.cityofnewyork.us/resource/k397-673e.json"

st.set_page_config(page_title="NYC Payroll Explorer", page_icon="📊", layout="wide")

st.title("NYC Payroll Explorer")
st.caption(
    "New York City publishes every city employee's payroll record. "
    "I spent 20+ years running payroll — here's what those numbers say to someone "
    "who has processed them for a living. Built with Python, pandas, and Streamlit."
)

# ---- Controls ------------------------------------------------
year = st.selectbox("Fiscal year", ["2025", "2024", "2023", "2022", "2021", "2020"])


# ---- Data loading (cached so the app stays fast) -------------
@st.cache_data(ttl=3600, show_spinner="Querying NYC Open Data...")
def query(soql: str) -> pd.DataFrame:
    """Run a SoQL query against NYC Open Data and return a DataFrame."""
    r = requests.get(API, params={"$query": soql}, timeout=30)
    r.raise_for_status()
    return pd.DataFrame(r.json())


# ==============================================================
# 1. WHERE DOES OVERTIME RUN HOT?
# ==============================================================
st.header("1. Where does overtime run hot?")

ot = query(f"""
    SELECT agency_name,
           sum(total_ot_paid) AS ot_paid,
           sum(regular_gross_paid) AS regular_paid,
           count(*) AS headcount
    WHERE fiscal_year = '{year}'
    GROUP BY agency_name
    ORDER BY sum(total_ot_paid) DESC
    LIMIT 10
""")

if not ot.empty:
    ot["ot_paid"] = pd.to_numeric(ot["ot_paid"])
    ot["regular_paid"] = pd.to_numeric(ot["regular_paid"])
    ot["ot_share_pct"] = (ot["ot_paid"] / (ot["regular_paid"] + ot["ot_paid"]) * 100).round(1)

    st.bar_chart(ot.set_index("agency_name")["ot_paid"], horizontal=True)
    st.dataframe(
        ot.rename(columns={
            "agency_name": "Agency",
            "ot_paid": "Total OT paid ($)",
            "regular_paid": "Regular gross ($)",
            "headcount": "Employees",
            "ot_share_pct": "OT as % of pay",
        }),
        hide_index=True,
        width='stretch',
    )
    st.markdown(
        "**A payroll professional's read:** overtime concentrating in a handful of agencies "
        "isn't a payroll quirk — it's a staffing signal. When OT runs above roughly 10–15% "
        "of total pay for a whole agency, year after year, it's usually cheaper on paper than "
        "hiring — but it shows up later as burnout, turnover, and errors. I've watched that "
        "trade-off play out from the payroll desk."
    )

# ==============================================================
# 2. WHAT DO CITY JOBS ACTUALLY PAY?
# ==============================================================
st.header("2. What do the biggest city jobs pay?")

titles = query(f"""
    SELECT title_description,
           count(*) AS headcount,
           avg(base_salary) AS avg_base
    WHERE fiscal_year = '{year}' AND pay_basis = 'per Annum'
    GROUP BY title_description
    ORDER BY count(*) DESC
    LIMIT 15
""")

if not titles.empty:
    titles["headcount"] = pd.to_numeric(titles["headcount"])
    titles["avg_base"] = pd.to_numeric(titles["avg_base"]).round(0)

    st.bar_chart(titles.set_index("title_description")["avg_base"], horizontal=True)
    st.dataframe(
        titles.rename(columns={
            "title_description": "Job title",
            "headcount": "Employees",
            "avg_base": "Average base salary ($)",
        }),
        hide_index=True,
        width='stretch',
    )
    st.markdown(
        "**A payroll professional's read:** I filtered this to salaried (*per Annum*) employees "
        "on purpose — for hourly staff, the `base_salary` field holds an hourly *rate*, and mixing "
        "the two silently wrecks any average. Knowing which fields mean what on a pay record is "
        "half of payroll work. Also note these are *averages*: a few long-tenured seniors in a "
        "title pull the number up, which is exactly why payroll reporting prefers medians when "
        "the system allows it."
    )

# ==============================================================
# 3. WHERE THE MONEY GOES, BY BOROUGH
# ==============================================================
st.header("3. Payroll footprint by borough")

boro = query(f"""
    SELECT work_location_borough,
           count(*) AS headcount,
           avg(base_salary) AS avg_base
    WHERE fiscal_year = '{year}'
      AND pay_basis = 'per Annum'
      AND work_location_borough IS NOT NULL
    GROUP BY work_location_borough
    ORDER BY count(*) DESC
    LIMIT 8
""")

if not boro.empty:
    boro["headcount"] = pd.to_numeric(boro["headcount"])
    boro["avg_base"] = pd.to_numeric(boro["avg_base"]).round(0)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Employees by borough")
        st.bar_chart(boro.set_index("work_location_borough")["headcount"])
    with col2:
        st.subheader("Average base salary")
        st.bar_chart(boro.set_index("work_location_borough")["avg_base"])
    st.markdown(
        "**A payroll professional's read:** headcount and pay don't distribute the same way — "
        "administrative and specialized roles cluster in Manhattan while field-heavy agencies "
        "spread across the boroughs. In payroll terms that's two different cost structures "
        "sharing one budget, and it's why location coding on every record matters more than "
        "people think."
    )

st.divider()
st.caption(
    "Data: NYC Open Data, Citywide Payroll Data (Fiscal Year) — queried live via the Socrata API. "
    "Built by Susana Fernandez Rivera · "
    "[Website](https://susanaef0903-source.github.io/personal-website/) · "
    "[GitHub](https://github.com/susanaef0903-source)"
)
