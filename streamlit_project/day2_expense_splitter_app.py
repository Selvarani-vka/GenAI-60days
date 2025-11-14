import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Splitter", page_icon="💸", layout="centered")

st.title("💸 Expense Splitter")

st.markdown("""
This app helps you split trip expenses among friends.
Enter everyone's contributions and expenses, and see who owes or gets back money.
""")

# --- Step 1: Number of People ---
num_people = st.number_input("👥 Number of People", min_value=2, max_value=20, step=1)

# --- Step 2: Get Names & Contributions ---
st.subheader("💰 Contributions")

names = []
contributions = []

for i in range(num_people):
    cols = st.columns([2, 1])
    name = cols[0].text_input(f"Name of person {i+1}", key=f"name_{i}")
    amount = cols[1].number_input(f"Contributed by {name or 'Person '+str(i+1)}", step=100.00, key=f"amount_{i}")
    if name:
        names.append(name)
        contributions.append(amount)

# --- Step 3: Expense Details ---
st.subheader("🧾 Expense Details")

st.markdown("Add total spending for each category:")

resort = st.number_input("🏕️ Resort",  step=100)
food = st.number_input("🍽️ Food",  step=100)
travel = st.number_input("🚗 Travel",  step=100)
other = st.number_input("🎟️ Other Expenses",  step=100)

# --- Step 4: Calculate Totals ---
if st.button("💥 Calculate Expense Split"):
    if len(names) != num_people:
        st.error("Please fill in all names before calculating.")
    else:
        total_contributed = sum(contributions)
        total_spent = resort + food + travel + other
        equal_share = total_spent / num_people if num_people > 0 else 0

        df = pd.DataFrame({
            "Name": names,
            "Contributed": contributions,
            "Share": [equal_share] * num_people,
        })
        df["Net"] = df["Contributed"] - df["Share"]

        st.success(f"🎯 Total Trip Expense: ₹{total_spent:,.2f}")
        st.info(f"Each person should pay: ₹{equal_share:,.2f}")

        st.dataframe(df.style.format({"Contributed": "₹{:.2f}", "Share": "₹{:.2f}", "Net": "₹{:.2f}"}))

        # --- Step 5: Show Who Owes or Gets Back ---
        st.subheader("📊 Settlement Summary")

        owes = df[df["Net"] < 0]
        gets = df[df["Net"] > 0]

        st.write("### People who owe money:")
        if owes.empty:
            st.write("✅ Nobody owes money.")
        else:
            for _, row in owes.iterrows():
                st.write(f"🔴 **{row['Name']}** owes ₹{abs(row['Net']):.2f}")

        st.write("### People who should get money back:")
        if gets.empty:
            st.write("✅ Nobody needs to be paid back.")
        else:
            for _, row in gets.iterrows():
                st.write(f"🟢 **{row['Name']}** should get back ₹{row['Net']:.2f}")


