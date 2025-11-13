import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Magical Unicorn Realm", layout="wide")

# --- Styling ---
page_style = """
<style>
.stApp {
    background: linear-gradient(135deg, #1a0033, #33004d, #000000);
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.header-box {
    background: linear-gradient(90deg, #ff69b4, #ffb6c1, #ffd700);
    color: black;
    font-weight: 900;
    font-size: 2rem;
    padding: 1rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 0 20px rgba(255, 182, 193, 0.6);
    margin: 1.5rem auto;
    max-width: 800px;
}

/* Labels */
label {
    font-weight: 800 !important;
    color: #ffccff !important;
    font-size: 1.2rem !important;
}

/* Buttons */
.stButton > button {
    background-color: #ff69b4 !important;
    color: white !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.2rem !important;
    border-radius: 15px !important;
    box-shadow: 0 0 10px #ff69b4;
    transition: background-color 0.3s ease;
}
.stButton > button:hover {
    background-color: #ff1493 !important;
}

/* Fade-in animation for image */
.fade-in {
    animation: fadeIn 1.2s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0; transform: scale(0.97);}
    to {opacity: 1; transform: scale(1);}
}

/* Centered text */
.center-text {
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 1rem;
}

/* Footer */
.footer {
    text-align: center;
    color: #ffc0cb;
    margin-top: 3rem;
    font-size: 1rem;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-box">🦄 Welcome to the Magical Unicorn 🦄</div>', unsafe_allow_html=True)

# --- Inputs ---
name = st.text_input("✨ Enter your name:")
age = st.slider("🎂 Select your age:", min_value=0, max_value=120, value=25)

sparkle_button = st.button("🌟 Show My Magical Unicorn 🌟")

# --- Display Logic ---
if sparkle_button:
    if name.strip():
        st.markdown(f"<h2 style='text-align:center;'>🌈 Hello, {name}! 🌈</h2>", unsafe_allow_html=True)

        # Select unicorn image based on age
        if age < 12:
            message = "You are young and full of wonder! 🧁 Meet your baby unicorn:"
            unicorn_file = "unicorn_kid.jpg"
        elif 12 <= age < 20:
            message = "A vibrant spirit full of dreams! 🌟 Here's your charming unicorn:"
            unicorn_file = "unicorn_teen.jpg"
        elif 20 <= age < 50:
            message = "A joyful adventurer! 🌈 Your unicorn shines bright:"
            unicorn_file = "unicorn_adult.jpg"
        else:
            message = "A timeless soul of magic! ✨ Meet your wise unicorn:"
            unicorn_file = "unicorn_elder.jpg"

        # Center the description text
        st.markdown(f"<p class='center-text'>{message}</p>", unsafe_allow_html=True)

        # Display the unicorn image centered with fade-in
        if os.path.exists(unicorn_file):
            unicorn_img = Image.open(unicorn_file)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
                st.image(unicorn_img, caption=f"{name}'s Magical Unicorn", width=400)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error(f"🦄 Oops! The unicorn image '{unicorn_file}' was not found. Please check the file path.")
    else:
        st.warning("Please enter your name before revealing your unicorn ✨")

# --- Footer ---
st.markdown('<div class="footer">🦄 Created with love and rainbow sparkles 💖</div>', unsafe_allow_html=True)
