import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import altair as alt
import os

# -----------------------------
# CSV FILE SETUP
# -----------------------------
FILE_PATH = "water_log.csv"

if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["date", "amount_ml", "timestamp"])
    df.to_csv(FILE_PATH, index=False)

df = pd.read_csv(FILE_PATH)

# Convert timestamp column to datetime
if not df.empty:
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["date"] = df["date"].astype(str)

st.set_page_config(page_title="Water Intake Tracker", page_icon="💧", layout="centered")

# -----------------------------
# HEADER
# -----------------------------
st.markdown("<h1>💧 Water Intake Tracker</h1>", unsafe_allow_html=True)

st.write("Log daily water intake (ml). Goal: **3 L (3000 ml)** per day.")

# -----------------------------
# INPUT: WATER INTAKE
# -----------------------------
amount_ml = st.number_input("Enter water intake (ml):", min_value=50, max_value=5000, value=150, step=50)

if st.button("Add Entry"):
    timestamp = datetime.now()
    entry_date = timestamp.date().isoformat()  # ← correct date extraction

    new_entry = {
        "date": entry_date,
        "amount_ml": amount_ml,
        "timestamp": timestamp
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)

    st.success(f"Added {amount_ml} ml")

# Refresh dataframe after update
df = pd.read_csv(FILE_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# -----------------------------
# TODAY’S ENTRIES
# -----------------------------
today_str = date.today().isoformat()
today_entries = df[df["date"] == today_str]

st.subheader("Entries for today")

if not today_entries.empty:
    st.dataframe(today_entries)

    if st.button("Reset today's entries"):
        df = df[df["date"] != today_str]
        df.to_csv(FILE_PATH, index=False)
        st.warning("Today's entries cleared")
else:
    st.info("No entries logged today yet.")

# -----------------------------
# WEEKLY HYDRATION — Rounded Pastel Bars
# -----------------------------
st.subheader("Weekly hydration (last 7 days) — pastel 🌈")

# Last 7 days
today = date.today()
start_date = today - timedelta(days=6)

week_days = pd.date_range(start=start_date, end=today)
weekly_df = pd.DataFrame({"date": week_days})

df["date"] = pd.to_datetime(df["date"], errors="coerce")

daily_totals = df.groupby("date")["amount_ml"].sum().reset_index()

weekly_merged = (
    weekly_df.merge(daily_totals, on="date", how="left")
    .fillna(0)
)

weekly_merged["label"] = weekly_merged["date"].dt.strftime("%a %d")

# Pastel color palette
pastel_color = "#A7C7E7"  # soft blue pastel

# Altair bar chart with rounded corners
chart = (
    alt.Chart(weekly_merged)
    .mark_bar(size=40, cornerRadiusTopLeft=10, cornerRadiusTopRight=10)
    .encode(
        x=alt.X("label:N", title="Day", sort=list(weekly_merged["label"])),
        y=alt.Y("amount_ml:Q", title="Total (ml)", scale=alt.Scale(domain=[0, weekly_merged["amount_ml"].max() + 500])),
        tooltip=[
            alt.Tooltip("label:N", title="Day"),
            alt.Tooltip("amount_ml:Q", title="Water (ml)")
        ],
        color=alt.value(pastel_color)
    )
    .properties(height=350)
)

st.altair_chart(chart, use_container_width=True)
st.caption("Rounded pastel bars = daily total. Goal = 3000 ml.")
