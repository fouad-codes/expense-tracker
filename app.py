import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Expense Tracker", layout="centered")

st.title("💸 Smart Student Expense Tracker")
st.markdown("Track smarter. Spend better. Stay broke… later 😄")

# Budget
budget = st.number_input("💰 Enter your monthly budget", min_value=0)

# Input section
st.subheader("➕ Add Expense")
amount = st.number_input("Amount", min_value=0)
category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Academics"])
add = st.button("Add Expense")

# Session state
if "data" not in st.session_state:
    st.session_state.data = []

if add and amount > 0:
    st.session_state.data.append({"Amount": amount, "Category": category})

df = pd.DataFrame(st.session_state.data)

# Show data
st.subheader("📋 Expense History")
st.write(df)

# Stats
if not df.empty:
    total = df["Amount"].sum()
    st.metric("💸 Total Spent", total)

    # Remaining
    if budget > 0:
        remaining = budget - total
        st.metric("💼 Remaining Budget", remaining)

        # Days until broke
        daily_avg = total / max(1, len(df))
        if daily_avg > 0:
            days_left = remaining / daily_avg
            st.warning(f"⚠️ Days Until Broke: {int(days_left)} days")

    # Pie chart
    st.subheader("📊 Spending Breakdown")
    category_sum = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%')
    st.pyplot(fig)

    # Smart insights (AI-like)
    st.subheader("🧠 Smart Insights")

    highest = category_sum.idxmax()
    st.info(f"📌 You are spending the most on **{highest}**")

    if highest == "Food":
        st.warning("🍔 Try reducing canteen/food expenses")
    elif highest == "Entertainment":
        st.warning("🎮 Cut down on entertainment spending")
    elif highest == "Transport":
        st.warning("🛵 Consider cheaper transport options")

else:
    st.info("Start adding expenses to see insights 👆")
