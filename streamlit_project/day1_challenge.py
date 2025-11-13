import streamlit as st

name=st.text_input("Enter your name:")

if st.button("hi"):
    if name:
        st.success(f"hello {name} welcome")
    else:
        st.warning("enter your name:")