import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Dashboard")

if "trip" in st.session_state:
    trip = st.session_state["trip"]
    st.success(f"📌 Current Trip: {trip['destination']}")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Destination", trip["destination"])
    with col2:
        st.metric("💰 Estimated Cost", f"₹{trip['estimate']:,}")
    with col3:
        st.metric("🎒 Budget", f"₹{trip['budget']:,}")

    st.markdown("---")

    # Detailed breakdown
    st.subheader("🧾 Detailed Cost Breakdown (Estimated)")
    breakdown = trip.get("breakdown", {})
    for key, value in breakdown.items():
        st.write(f"**{key}**: ₹{value:,}")

    # Show actuals if available
    actuals = trip.get("actuals")
    if actuals:
        st.subheader("🧾 Actual Expenses (Saved)")
        for key, value in actuals.items():
            st.write(f"**{key}**: ₹{value:,}")
    else:
        st.info("No actual expenses saved yet. Add them in Manage Expenses.")

    # Budget status
    diff = trip["budget"] - trip["estimate"]
    st.markdown("---")
    if diff >= 0:
        st.success(f"✅ Within Budget! You save ₹{diff:,}")
    else:
        st.error(f"⚠ Over Budget by ₹{-diff:,}")

    # Progress: percent of budget estimated
    used_pct = min(trip["estimate"] / max(trip["budget"], 1), 1.0)
    st.write("### 🔢 Budget Usage (based on estimate)")
    st.progress(used_pct)

    st.markdown("---")

    # Charts
    st.subheader("📊 Estimated vs Actual Expenses")

    categories = ["HotelCost", "FoodCost", "ActivitiesCost", "TransportCost"]
    estimated = [breakdown.get(c, 0) for c in categories]

    if actuals:
        actual = [actuals.get(c, 0) for c in categories]
    else:
        # fallback: estimated + 10%
        actual = [int(v * 1.10) for v in estimated]

    # Bar chart
    def show_bar_chart():
        plt.figure(figsize=(8, 5))
        x = range(len(categories))
        labels = ["Hotel", "Food", "Activities", "Transport"]

        plt.bar(x, estimated, width=0.4, label="Estimated")
        plt.bar([p + 0.4 for p in x], actual, width=0.4, label="Actual")

        plt.xlabel("Expense Categories")
        plt.ylabel("Amount (₹)")
        plt.title("Estimated vs Actual Trip Expenses")
        plt.xticks([p + 0.2 for p in x], labels, rotation=0)
        plt.legend()
        plt.tight_layout()
        st.pyplot(plt)

    show_bar_chart()

    st.markdown("---")

    # Pie chart for estimated breakdown
    st.subheader("🟠 Expense Distribution (Estimated)")
    def show_pie_chart():
        plt.figure(figsize=(5, 5))
        labels = ["Hotel", "Food", "Activities", "Transport"]
        sizes = estimated
        # avoid zero-only pie error
        if sum(sizes) == 0:
            st.info("No estimated costs to show in pie chart.")
            return
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Estimated Cost Share")
        plt.tight_layout()
        st.pyplot(plt)

    show_pie_chart()

    st.markdown("---")

    # Totals
    est_total = sum(estimated)
    act_total = sum(actual) if actual else None

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Estimated Total", f"₹ {est_total:,}")
    with col2:
        st.metric("Actual Total", f"₹ {act_total:,}" if act_total else "—")

else:
    st.info("Plan a trip to view dashboard info 🧭")
