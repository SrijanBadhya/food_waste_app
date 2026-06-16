# pylint: disable=no-member, invalid-name
import random
import streamlit as st


# 1. INITIAL SETUP / DATA STORAGE
if "food_produced" not in st.session_state:
    st.session_state.food_produced = random.randint(50, 150)  # nosec # Randomized [cite: 203] 
if "food_consumed" not in st.session_state:
    # Must be less than or equal to production [cite: 204]
    st.session_state.food_consumed = random.randint( # nosec
        10, st.session_state.food_produced
    )
if "food_status" not in st.session_state:
    st.session_state.food_status = "At Restaurant"  # Initial status [cite: 201]


# 2. CORE MATHEMATICAL LOGIC FUNCTIONS
def calculate_availability(produced, consumed):
    """Calculate remaining food[cite: 194, 205]."""
    return max(0, produced - consumed)


def calculate_trucks_needed(available_food, food_per_truck=20):
    """Calculate dynamic truck number based on leftover food[cite: 195, 206]."""
    if available_food <= 0:
        return 0
    # Simple ceiling division
    return (available_food + food_per_truck - 1) // food_per_truck


# 3. UI
st.title("Food Waste Reduction Platform")

# Display Current Stats [cite: 205]
st.subheader("Daily Logistics Console")
st.text(f"Food Produced: {st.session_state.food_produced} kg")
st.text(f"Food Consumed: {st.session_state.food_consumed} kg")

available = calculate_availability(
    st.session_state.food_produced, st.session_state.food_consumed
)
st.metric(label="Available Food Remaining", value=f"{available} kg")

# Truck Calculator [cite: 206]
trucks = calculate_trucks_needed(available)
st.metric(label="Trucks Required Today (20 kg capacity each)", value=trucks)

st.write("---")

# Status Tracker & Buttons [cite: 208, 209]
st.subheader("Food Status Tracker")
st.info(f"Current Status: {st.session_state.food_status}")

col1, col2 = st.columns(2)
with col1:
    if st.button("Transfer to Truck"):
        st.session_state.food_status = "In Transport"  # [cite: 201, 208]
with col2:
    if st.button("Transfer to Destination"):
        st.session_state.food_status = "Reached NGO Destination"  # [cite: 201, 208]

st.write("---")

# Day Changer Button 
if st.button("⚠️ Click to Change Day (Reset System)"):
    st.session_state.food_produced = random.randint(50, 150) # nosec # New random production for the next day [cite: 203]
    st.session_state.food_consumed = random.randint( # nosec
        10, st.session_state.food_produced
    )
    st.session_state.food_status = "At Restaurant"
    st.success("System reset for the next day!")