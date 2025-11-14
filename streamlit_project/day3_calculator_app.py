import streamlit as st

# Set page config
st.set_page_config(page_title="Simple Calculator", page_icon="🧮")

# Title
st.title("🧮 Simple Calculator")

# Result display
st.subheader("Result")
result_placeholder = st.empty()

# Input fields
col1, col2, col3 = st.columns(3)

with col1:
    num1 = st.number_input("First number", value=0.0)

with col2:
    num2 = st.number_input("Second number", value=0.0)

with col3:
    operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])

# Perform calculation
result = None

if operation == "Add":
    result = num1 + num2
elif operation == "Subtract":
    result = num1 - num2
elif operation == "Multiply":
    result = num1 * num2
elif operation == "Divide":
    if num2 != 0:
        result = num1 / num2
    else:
        result_placeholder.error("Error: Division by zero is not allowed.")

# Display result if valid
if result is not None:
    result_placeholder.success(f"{result}")

