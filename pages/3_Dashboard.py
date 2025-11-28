import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Dashboard")

if "trip" in st.session_state:
    trip = st.session_state["trip"]
    st.success(f"📌 Current Trip: {trip['destination']}")

    # -------------------------------
    # Display trip summary cards
    # -------------------------------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Destination", trip["destination"])
    with col2:
        st.metric("💰 Estimated Cost", f"₹{trip['estimate']:,}")
    with col3:
        st.metric("🎒 Budget", f"₹{trip['budget']:,}")

    st.markdown("---")

    # -------------------------------
    # Detailed cost breakdown from trip session
    # -------------------------------
    st.subheader("🧾 Detailed Cost Breakdown")
    for key, value in trip["breakdown"].items():
        st.write(f"**{key}**: ₹{value:,}")

    # Budget Status
    diff = trip["budget"] - trip["estimate"]
    st.markdown("---")
    if diff >= 0:
        st.success(f"✅ Within Budget! You save ₹{diff:,}")
    else:
        st.error(f"⚠ Over Budget by ₹{-diff:,}")

    st.markdown("---")

    # ----------------------------------
    # 📊 Estimated vs Actual Expense Chart
    # ----------------------------------
    st.subheader("📊 Estimated vs Actual Expenses")

    # Extract values
    categories = list(trip["breakdown"].keys())
    estimated = list(trip["breakdown"].values())

    # Fake actual values (10% variance) – replace later with real expenses
    actual = [val * 1.10 for val in estimated]

    # Chart function
    def show_bar_chart():
        plt.figure(figsize=(8, 5))
        x = range(len(categories))

        plt.bar(x, estimated, width=0.4, label="Estimated")
        plt.bar([p + 0.4 for p in x], actual, width=0.4, label="Actual")

        plt.xlabel("Expense Categories")
        plt.ylabel("Amount (₹)")
        plt.title("Estimated vs Actual Trip Expenses")
        plt.xticks([p + 0.2 for p in x], categories, rotation=0)
        plt.legend()
        plt.tight_layout()

        st.pyplot(plt)

    show_bar_chart()

else:
    st.info("Plan a trip to view dashboard info 🧭")
