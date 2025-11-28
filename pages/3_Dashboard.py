import streamlit as st

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Dashboard")

if "trip" in st.session_state:
    trip = st.session_state["trip"]
    st.success(f"📌 Current Trip: {trip['destination']}")

    # Display trip summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Destination", trip["destination"])
    with col2:
        st.metric("💰 Estimated Cost", f"₹{trip['estimate']:,}")
    with col3:
        st.metric("🎒 Budget", f"₹{trip['budget']:,}")

    st.markdown("---")

    st.subheader("🧾 Detailed Cost Breakdown")
    for key, value in trip["breakdown"].items():
        st.write(f"**{key}**: ₹{value:,}")

    # Budget Status Indicator
    diff = trip["budget"] - trip["estimate"]
    st.markdown("---")
    if diff >= 0:
        st.success(f"✅ Within Budget! You save ₹{diff:,}")
    else:
        st.error(f"⚠ Over Budget by ₹{-diff:,}")

else:
    st.info("Plan a trip to view dashboard info 🧭")




