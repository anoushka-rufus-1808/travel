import streamlit as st

st.set_page_config(page_title="Expenses", page_icon="💰")

st.title("💰 Travel Expense Manager")

if "trip" not in st.session_state:
    st.warning("First plan a trip from Plan Trip page 🧭")
    st.stop()

trip = st.session_state["trip"]

if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

expense_name = st.text_input("Expense Name")
expense_amount = st.number_input("Amount (₹)", 0)

if st.button("Add Expense ➕"):
    st.session_state["expenses"].append({"name": expense_name, "cost": expense_amount})

total_spent = sum(x["cost"] for x in st.session_state["expenses"])

st.subheader("🧾 Expense List")
st.table(st.session_state["expenses"])

remaining = trip["estimate"] - total_spent

st.metric("Remaining vs Estimated", f"₹{remaining:,}")



