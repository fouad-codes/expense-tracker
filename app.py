import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("Student Expense Tracker")
st.write("Track your spending and manage your monthly budget.")

# Budget input
budget = st.number_input("Enter your monthly budget", min_value=0)

# Expense input
st.subheader("Add Expense")

amount = st.number_input("Amount", min_value=0)

category = st.selectbox(
    "Category",
    [
        "Food",
        "Transport",
        "Entertainment",
        "Academics",
        "Shopping",
        "Health",
        "Subscriptions",
        "Other"
    ]
)

add_expense = st.button("Add Expense")

# Initialize session data
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Add new expense
if add_expense and amount > 0:
    st.session_state.expenses.append({
        "Amount": amount,
        "Category": category
    })

# Convert to DataFrame
df = pd.DataFrame(st.session_state.expenses)

# Expense history
st.subheader("Expense History")

if not df.empty:

    for index, row in df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])

        col1.write(f"₹{row['Amount']}")
        col2.write(row["Category"])

        if col3.button("Remove", key=index):
            st.session_state.expenses.pop(index)
            st.rerun()

    # Summary metrics
    total_spent = df["Amount"].sum()
    st.write(f"Total spent: ₹{total_spent}")

    if budget > 0:
        remaining = budget - total_spent
        st.write(f"Remaining budget: ₹{remaining}")

        average_spending = total_spent / max(1, len(df))

        if average_spending > 0:
            days_left = remaining / average_spending
            st.write(f"Estimated days until budget runs out: {int(days_left)}")

    # Spending chart
    st.subheader("Spending Breakdown")

    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(category_totals, labels=category_totals.index, autopct="%1.1f%%")

    st.pyplot(fig)

    # Basic insight
    st.subheader("Insights")

    highest_category = category_totals.idxmax()
    st.write(f"Highest spending category: {highest_category}")

else:
    st.write("No expenses recorded yet.")
