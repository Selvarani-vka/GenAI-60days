import streamlit as st
import requests

st.set_page_config(page_title="Converter", layout="centered", initial_sidebar_state="collapsed")

# -------------------------
# Robust CSS (background + inputs + containers)
# Multiple selectors used so it applies across Streamlit versions/themes
# -------------------------
st.markdown(
    """
    <style>
    /* App background (robust selectors) */
    html, body, .stApp, .main, [data-testid="stAppViewContainer"], .block-container {
        background: linear-gradient(180deg, #f3f7ff 0%, #eef6ff 50%, #f8fbff 100%) !important;
        color: #0b2545;
    }

    /* Page title spacing */
    .page-title {
        margin-top: 6px;
        margin-bottom: 6px;
    }

    /* Card-like container for sections */
    .card {
        background: white;
        padding: 20px 22px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(11,37,69,0.06);
        border: 1px solid rgba(11,37,69,0.04);
        margin-bottom: 18px;
    }

    /* Section heading */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #1f3b5a;
    }

    /* Stylish smaller divider (non-empty, subtle) */
    .sub-divider {
        height: 12px;
        border-radius: 8px;
        background: linear-gradient(90deg, rgba(11,102,255,0.04), rgba(11,102,255,0.01));
        margin: 12px 0 18px 0;
    }

    /* Input styling:
       Target actual input elements for consistent appearance */
    input[type="number"], input[type="text"], textarea {
        background-color: #fbfdff;
        border: 1px solid #e7f0ff;
        padding: 10px 12px;
        border-radius: 10px;
        font-size: 15px;
        color: #0b2545;
        box-shadow: none;
    }

    /* Decrease default Streamlit top padding (avoid a big empty area) */
    .block-container {
        padding-top: 18px;
        padding-left: 40px;
        padding-right: 40px;
        padding-bottom: 40px;
    }

    /* Remove large default margins for headings that sometimes create blank space */
    .stMarkdown h1, .stMarkdown h2 {
        margin: 6px 0 10px 0;
    }

    /* Tighter number input width */
    .stNumberInput > label {
        font-size: 13px;
        color: #334e6f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Helper: fetch INR->USD rate (cached)
# -------------------------
@st.cache_data(ttl=300)
def fetch_rate():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/INR", timeout=6)
        r.raise_for_status()
        data = r.json()
        return float(data["rates"]["USD"])
    except Exception:
        return None

rate = fetch_rate()

# -------------------------
# Page header (no empty placeholder)
# -------------------------
st.markdown("<div style='display:flex;align-items:center;gap:12px'>"
            "<div style='font-size:30px'>🔁</div>"
            "<div><h1 class='page-title' style='margin:0'>Converter</h1>"
            "<div style='color:#3b5f8a;font-weight:600'>Realtime updates on change</div></div></div>",
            unsafe_allow_html=True)

# -------------------------
# Currency Section
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>💱 Currency (INR ⇄ USD)</div>", unsafe_allow_html=True)

if rate is not None:
    st.success(f"Live Rate Loaded: 1 INR = {rate:.4f} USD")
else:
    st.warning("Could not load live INR → USD rate. Currency conversion will be disabled.")

# initialize numeric session state values if missing
if "rate" not in st.session_state:
    st.session_state.rate = rate or 0.0
if "inr" not in st.session_state:
    st.session_state.inr = 100.0
if "usd" not in st.session_state:
    st.session_state.usd = round(st.session_state.inr * st.session_state.rate, 4) if st.session_state.rate else 0.0

# two-way callbacks (store numeric floats)
def update_usd():
    try:
        v = float(st.session_state.inr)
        st.session_state.usd = round(v * st.session_state.rate, 4)
    except:
        st.session_state.usd = 0.0

def update_inr():
    try:
        v = float(st.session_state.usd)
        st.session_state.inr = round(v / st.session_state.rate, 4)
    except:
        st.session_state.inr = 0.0

c1, c2 = st.columns([1,1], gap="large")
with c1:
    st.number_input("INR", key="inr", min_value=0.0, step=1.0, format="%.4f", on_change=update_usd)
with c2:
    st.number_input("USD", key="usd", min_value=0.0, step=0.01, format="%.4f", on_change=update_inr)

st.markdown("</div>", unsafe_allow_html=True)

# subtle divider (no big blank box)
st.markdown("<div class='sub-divider'></div>", unsafe_allow_html=True)

# -------------------------
# Temperature Section
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>🌡 Temperature (°C ⇄ °F)</div>", unsafe_allow_html=True)

if "c" not in st.session_state: st.session_state.c = 25.0
if "f" not in st.session_state: st.session_state.f = round((st.session_state.c * 9/5) + 32, 2)

def c_to_f_cb():
    try:
        c = float(st.session_state.c)
        st.session_state.f = round((c * 9/5) + 32, 2)
    except:
        st.session_state.f = 0.0

def f_to_c_cb():
    try:
        f = float(st.session_state.f)
        st.session_state.c = round((f - 32) * 5/9, 2)
    except:
        st.session_state.c = 0.0

t1, t2 = st.columns([1,1], gap="large")
with t1:
    st.number_input("°C", key="c", format="%.2f", on_change=c_to_f_cb)
with t2:
    st.number_input("°F", key="f", format="%.2f", on_change=f_to_c_cb)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-divider'></div>", unsafe_allow_html=True)

# -------------------------
# Length Section
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📏 Length (cm ⇄ inch)</div>", unsafe_allow_html=True)

if "cm" not in st.session_state: st.session_state.cm = 10.0
if "inch" not in st.session_state: st.session_state.inch = round(st.session_state.cm / 2.54, 4)

def cm_to_inch_cb():
    try:
        cm = float(st.session_state.cm)
        st.session_state.inch = round(cm / 2.54, 4)
    except:
        st.session_state.inch = 0.0

def inch_to_cm_cb():
    try:
        inch = float(st.session_state.inch)
        st.session_state.cm = round(inch * 2.54, 4)
    except:
        st.session_state.cm = 0.0

l1, l2 = st.columns([1,1], gap="large")
with l1:
    st.number_input("cm", key="cm", format="%.4f", on_change=cm_to_inch_cb)
with l2:
    st.number_input("inch", key="inch", format="%.4f", on_change=inch_to_cm_cb)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-divider'></div>", unsafe_allow_html=True)

# -------------------------
# Weight Section
# -------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>⚖ Weight (kg ⇄ lb)</div>", unsafe_allow_html=True)

if "kg" not in st.session_state: st.session_state.kg = 70.0
if "lb" not in st.session_state: st.session_state.lb = round(st.session_state.kg * 2.20462, 4)

def kg_to_lb_cb():
    try:
        kg = float(st.session_state.kg)
        st.session_state.lb = round(kg * 2.20462, 4)
    except:
        st.session_state.lb = 0.0

def lb_to_kg_cb():
    try:
        lb = float(st.session_state.lb)
        st.session_state.kg = round(lb / 2.20462, 4)
    except:
        st.session_state.kg = 0.0

w1, w2 = st.columns([1,1], gap="large")
with w1:
    st.number_input("kg", key="kg", format="%.4f", on_change=kg_to_lb_cb)
with w2:
    st.number_input("lb", key="lb", format="%.4f", on_change=lb_to_kg_cb)

st.markdown("</div>", unsafe_allow_html=True)
