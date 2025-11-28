import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Trip", page_icon="🧭")

st.title("🧭 Plan Trip")

@st.cache_data
def load_tour_data():
    return pd.read_csv("india_tour_data.csv")

df = load_tour_data()

st.write("### Choose a destination")
dest = st.selectbox("Destination", df["Destination"].sort_values().unique())

# Get row for selected destination
row = df[df["Destination"] == dest].iloc[0]

st.write("### Estimated costs")
col1, col2 = st.columns(2)
with col1:
    st.metric("Hotel (per person)", f"₹ {int(row['HotelCost']):,}")
    st.metric("Food (per person)", f"₹ {int(row['FoodCost']):,}")
with col2:
    st.metric("Activities (per person)", f"₹ {int(row['ActivitiesCost']):,}")
    st.metric("Transport (per person)", f"₹ {int(row['TransportCost']):,}")

st.markdown("---")
st.write("### Trip settings")
num_people = st.number_input("Number of travellers", min_value=1, value=1)
days = st.number_input("Number of days", min_value=1, value=1)
budget = st.number_input("Your total budget (₹)", min_value=0, value=int((row['HotelCost']+row['FoodCost']+row['ActivitiesCost']+row['TransportCost'])*num_people))

if st.button("Create Trip"):
    # Breakdown (per person * people * days if needed — here keep per trip simple)
    breakdown = {
        "HotelCost": int(row["HotelCost"]) * num_people,
        "FoodCost": int(row["FoodCost"]) * num_people,
        "ActivitiesCost": int(row["ActivitiesCost"]) * num_people,
        "TransportCost": int(row["TransportCost"]) * num_people
    }
    estimated_total = sum(breakdown.values())

    trip = {
        "destination": dest,
        "days": int(days),
        "people": int(num_people),
        "budget": int(budget),
        "estimate": int(estimated_total),
        "breakdown": breakdown,
        # actuals will be filled by Manage Expenses later
        "actuals": None
    }

    st.session_state["trip"] = trip
    st.success(f"Trip created for {dest}. Estimated total: ₹{estimated_total:,}")
    #st.experimental_rerun()
