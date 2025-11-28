import streamlit as st

st.set_page_config(page_title="Manage Expenses", page_icon="💰")

st.title("💰 Manage Expenses")

if "trip" not in st.session_state:
    st.info("Plan a trip first (Go to Plan Trip).")
else:
    trip = st.session_state["trip"]
    st.success(f"Managing expenses for: {trip['destination']}")

    st.write("### Enter actual expenses (total amounts)")
    breakdown = trip.get("breakdown", {})
    default_hotel = int(breakdown.get("HotelCost", 0))
    default_food = int(breakdown.get("FoodCost", 0))
    default_activities = int(breakdown.get("ActivitiesCost", 0))
    default_transport = int(breakdown.get("TransportCost", 0))

    with st.form("actuals_form"):
        hotel_spent = st.number_input("Hotel spent (₹)", min_value=0, value=default_hotel)
        food_spent = st.number_input("Food spent (₹)", min_value=0, value=default_food)
        activities_spent = st.number_input("Activities spent (₹)", min_value=0, value=default_activities)
        transport_spent = st.number_input("Transport spent (₹)", min_value=0, value=default_transport)

        submitted = st.form_submit_button("Save Actuals")

        if submitted:
            actuals = {
                "HotelCost": int(hotel_spent),
                "FoodCost": int(food_spent),
                "ActivitiesCost": int(activities_spent),
                "TransportCost": int(transport_spent)
            }
            actual_total = sum(actuals.values())

            # Save to session_state
            st.session_state["actual_expenses"] = actuals
            # also attach to trip for dashboard convenience
            st.session_state["trip"]["actuals"] = actuals
            st.session_state["trip"]["actual_total"] = int(actual_total)

            st.success(f"Saved actuals. Actual total: ₹{actual_total:,}")
            st.experimental_rerun()

    # Option to clear actuals
    if "actuals" in trip and trip["actuals"]:
        if st.button("Clear saved actuals"):
            st.session_state["trip"]["actuals"] = None
            st.session_state["trip"]["actual_total"] = None
            if "actual_expenses" in st.session_state:
                del st.session_state["actual_expenses"]
            st.success("Cleared actual expenses.")
            st.experimental_rerun()
