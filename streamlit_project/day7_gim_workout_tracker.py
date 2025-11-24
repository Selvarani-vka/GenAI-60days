import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.graph_objects as go

# ========================================================
#               MOBILE APP THEME + STYLE
# ========================================================

mobile_style = """
<style>

body, .stApp {
    background: #eefdcc; /* soft charming green */
}

/* Mobile Header */
.mobile-title {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    padding: 10px 0 0 0;
    color: #273b25;
}

/* Section Title */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 10px;
    margin-bottom: 8px;
    color: #1f331d;
}

/* Card Style */
.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton>button {
    background: #4CAF50 !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-size: 17px !important;
    width: 100%;
}

/* Inputs → Mobile-like rounded fields */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stDateInput>div>div>input {
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 16px !important;
}

/* ===========================
   FINAL SELECTBOX FIX
   =========================== */

.stSelectbox div[data-baseweb="select"] {
    min-height: 48px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 12px !important;
    border-radius: 12px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    padding: 0 !important;
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
    line-height: 22px !important;
}

/* Dropdown Arrow */
.stSelectbox div[data-baseweb="select"] svg {
    margin-top: 0 !important;
    align-self: center !important;
}

/* Dropdown Items */
ul[role="listbox"] li {
    padding: 10px 14px !important;
    font-size: 16px !important;
    line-height: 22px !important;
    color: #222 !important;
}

ul[role="listbox"] {
    border-radius: 10px !important;
}

</style>
"""

st.markdown(mobile_style, unsafe_allow_html=True)

# ========================================================
#           DATA LOADING AND SAVING
# ========================================================

DATA_FILE = "workout_log.csv"

try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight"])

# Ensure date is NOT datetime (for table display)
if "date" in df.columns:
    df["date"] = df["date"].astype(str)

# ========================================================
#          AUTO-SUGGEST EXERCISES LIST
# ========================================================

COMMON_EXERCISES = [
    "Bench Press", "Incline Press", "Chest Fly", "Push Ups",
    "Lat Pulldown", "Deadlift", "Pull Ups", "Seated Row",
    "Bicep Curl", "Hammer Curl", "Tricep Extension",
    "Shoulder Press", "Lateral Raise", "Leg Press",
    "Squat", "Lunges", "Leg Curl", "Leg Extension"
]

# ========================================================
#           MOBILE HEADER
# ========================================================

st.markdown("<div class='mobile-title'>🏋️ Gym Workout Logger</div>", unsafe_allow_html=True)
st.write("")

# ========================================================
#                CARD 1 — ADD WORKOUT
# ========================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Add Workout</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    log_date = st.date_input("Date", value=date.today())
with col2:
    exercise = st.selectbox("Exercise (Auto-Suggest)", COMMON_EXERCISES)

col3, col4, col5 = st.columns(3)
with col3:
    sets = st.number_input("Sets", min_value=1, value=3)
with col4:
    reps = st.number_input("Reps", min_value=1, value=10)
with col5:
    weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0)

if st.button("Save Workout"):
    new_row = {
        "date": log_date.isoformat(),
        "exercise": exercise,
        "sets": sets,
        "reps": reps,
        "weight": weight,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Workout saved!")

st.markdown("</div>", unsafe_allow_html=True)


# ========================================================
#              CARD 2 — VIEW HISTORY
# ========================================================

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Workout History</div>", unsafe_allow_html=True)

# FIX: Make sure date column is always string for display
try:
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
except:
    pass

if df.empty:
    st.info("No workouts logged yet.")
else:
    st.dataframe(df, hide_index=True, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
#  CARD 3: WEEKLY PROGRESS (PLOTLY MOBILE CHART)
# =========================================================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Weekly Progress</div>", unsafe_allow_html=True)

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    df["volume"] = df["sets"] * df["reps"] * df["weight"]

    end = date.today()
    start = end - timedelta(days=6)

    week_df = df[(df["date"] >= pd.to_datetime(start)) & (df["date"] <= pd.to_datetime(end))]

    if not week_df.empty:
        week_df["day"] = week_df["date"].dt.date
        daily_volume = week_df.groupby("day")["volume"].sum().reset_index()

        # Create a stylish gradient area chart
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_volume["day"],
            y=daily_volume["volume"],
            mode='lines+markers',
            line=dict(color="#4CAF50", width=4),
            marker=dict(size=10, color="#2E7D32"),
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.25)',
            hovertemplate="<b>%{x}</b><br>Volume: %{y}<extra></extra>"
        ))

        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="",
            yaxis_title="Total Volume",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14, color="#1b331b")
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No workouts in the last 7 days.")
else:
    st.info("Log workouts to see progress.")

st.markdown("</div>", unsafe_allow_html=True)
