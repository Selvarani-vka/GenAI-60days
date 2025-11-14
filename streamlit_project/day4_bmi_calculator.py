import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

# ---------- CSS ----------
st.markdown("""
    <style>
        .title {
            font-size: 32px;
            text-align: center;
            font-weight: bold;
            color: #ffffff;
        }
        .result-box {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
            color: #000000;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>BMI Calculator</div>", unsafe_allow_html=True)

# ---------- SESSION STATE INIT ----------
if "bmi" not in st.session_state:
    st.session_state.bmi = None
if "category" not in st.session_state:
    st.session_state.category = None

# ---------- RESULT DISPLAY ----------
if st.session_state.bmi:
    st.markdown(
        f"<div class='result-box'><h3>BMI: {st.session_state.bmi}</h3></div>",
        unsafe_allow_html=True
    )

if st.session_state.category:
    st.markdown(
        f"<div class='result-box'><h3>Category: {st.session_state.category}</h3></div>",
        unsafe_allow_html=True
    )

# ---------- INPUTS ----------
st.write("### Enter your details:")
col1, col2 = st.columns(2)

height = col1.number_input("Height (cm)", min_value=50, max_value=250, value=170)
weight = col2.number_input("Weight (kg)", min_value=10, max_value=300, value=70)

# ---------- BUTTONS ----------
col_a, col_b = st.columns(2)

calculate = col_a.button("Calculate BMI")
clear = col_b.button("Clear Results")

# ---------- CALCULATE ACTION ----------
if calculate:
    height_m = height / 100
    bmi_value = round(weight / (height_m ** 2), 2)

    # Update session state
    st.session_state.bmi = bmi_value

    # Category logic
    if bmi_value < 18.5:
        st.session_state.category = "Underweight"
    elif bmi_value < 25:
        st.session_state.category = "Normal"
    elif bmi_value < 30:
        st.session_state.category = "Overweight"
    else:
        st.session_state.category = "Obese"

    st.rerun()  # Refresh page to show results instantly

# ---------- CLEAR ACTION ----------
if clear:
    st.session_state.bmi = None
    st.session_state.category = None
    st.rerun()
