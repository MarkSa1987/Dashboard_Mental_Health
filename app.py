import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- Load Data ----------
df = pd.read_csv("cleaned_survey.csv")

st.set_page_config(page_title="Mental Health Dashboard", layout="wide")
st.title("🧠 Mental Health in the Tech Industry Dashboard")

# ---------- Sidebar Filters ----------
with st.sidebar:
    st.header("Filters")

    gender = st.selectbox("Gender", ["All"] + sorted(df["Gender"].dropna().unique()))
    country = st.selectbox("Country", ["All"] + sorted(df["Country"].dropna().unique()))
    remote = st.selectbox("Remote Work", ["All"] + sorted(df["remote_work"].dropna().unique()))
    company_size = st.selectbox("Company Size", ["All"] + sorted(df["no_employees"].dropna().unique()))

# ---------- Apply Filters ----------
df_filtered = df.copy()

if gender != "All":
    df_filtered = df_filtered[df_filtered["Gender"] == gender]

if country != "All":
    df_filtered = df_filtered[df_filtered["Country"] == country]

if remote != "All":
    df_filtered = df_filtered[df_filtered["remote_work"] == remote]

if company_size != "All":
    df_filtered = df_filtered[df_filtered["no_employees"] == company_size]

# ---------- Create a 2×2 Grid Layout ----------
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# ---- Q1: Age & Gender vs Treatment ----
with row1_col1:
    st.subheader("Treatment by Age")
    fig1 = px.histogram(
        df_filtered,
        x="Age",
        color="treatment",
        barmode="group",
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---- Q2: Family History vs Treatment ----
with row1_col2:
    st.subheader("Family History ↔︎ Treatment")
    fig2 = px.histogram(
        df_filtered,
        x="family_history",
        color="treatment",
        barmode="group",
        height=350
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---- Q3: Supervisor Comfort vs Company Size ----
with row2_col1:
    st.subheader("Comfort Discussing MH with Supervisor by Company Size")
    fig3 = px.histogram(
        df_filtered,
        x="no_employees",
        color="supervisor",
        barmode="group",
        category_orders={
            "no_employees": [
                "1-5", "6-25", "26-100", "100-500",
                "500-1000", "More than 1000"
            ]
        },
        height=350
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---- Q4: Country vs Treatment Choropleth ----
with row2_col2:
    st.subheader("Treatment Counts by Country")
    country_ct = (
        df_filtered[df_filtered["Country"].notna()]
        .groupby(["Country", "treatment"])
        .size()
        .reset_index(name="count")
    )
    fig4 = px.choropleth(
        country_ct,
        locations="Country",
        locationmode="country names",
        color="count",
        hover_name="treatment",
        height=350
    )
    st.plotly_chart(fig4, use_container_width=True)
