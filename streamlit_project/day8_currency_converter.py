import streamlit as st

st.set_page_config(page_title="Currency Converter", layout="centered")

# Background styling
st.markdown("""
<style>
.stApp {
    background-color: #89CFF0 !important;
}
.currency-box {
    background: #fff;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.18);
    margin-top: 20px;
}
h1 {
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

RATES = {
    "INR": 1,
    "USD": 83,
    "EUR": 90,
    "GBP": 105,
}

def convert(value, base):
    in_inr = value * RATES[base]
    return {k: round(in_inr / RATES[k], 2) for k in RATES}

# Initialize session state
for c in RATES:
    st.session_state.setdefault(c, 0.0)

# UI
st.markdown("<h1>💱 Currency Converter</h1>", unsafe_allow_html=True)
st.markdown("<div class='currency-box'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

def number_input_callback(changed_key):
    val = st.session_state[changed_key]
    results = convert(val, changed_key)
    for c, v in results.items():
        if c != changed_key:
            st.session_state[c] = v

with col1:
    st.number_input("INR", key="INR", value=st.session_state["INR"], step=0.01,
                    on_change=lambda: number_input_callback("INR"))
    st.number_input("USD", key="USD", value=st.session_state["USD"], step=0.01,
                    on_change=lambda: number_input_callback("USD"))

with col2:
    st.number_input("EUR", key="EUR", value=st.session_state["EUR"], step=0.01,
                    on_change=lambda: number_input_callback("EUR"))
    st.number_input("GBP", key="GBP", value=st.session_state["GBP"], step=0.01,
                    on_change=lambda: number_input_callback("GBP"))

st.markdown("</div>", unsafe_allow_html=True)

