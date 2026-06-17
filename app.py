# pylint: disable=no-member, invalid-name
"""MODULE DOCSTRING:

This Streamlit app simulates a food waste reduction platform for restaurants.
"""

import random
import time
import streamlit as st

# ==========================================
# 1. INITIAL SETUP / DATA STORAGE
# ==========================================
if "food_produced" not in st.session_state:
    st.session_state.food_produced = random.randint(50, 150)  # nosec
if "food_consumed" not in st.session_state:
    st.session_state.food_consumed = random.randint(  # nosec
        10, st.session_state.food_produced
    )

# Track statuses and timestamps for each of the 3 possible trucks
for i in range(1, 4):
    if f"truck_{i}_status" not in st.session_state:
        st.session_state[f"truck_{i}_status"] = "Ready at Restaurant"
    if f"truck_{i}_dispatch_time" not in st.session_state:
        st.session_state[f"truck_{i}_dispatch_time"] = None


# ==========================================
# 2. AUTOMATIC 30-SECOND TIME CHECKER
# ==========================================
# This loops through active trucks and handles background state updates cleanly
current_time = time.time()
for i in range(1, 4):
    if st.session_state[f"truck_{i}_status"] == "In Transport":
        dispatch_time = st.session_state[f"truck_{i}_dispatch_time"]
        if dispatch_time and (current_time - dispatch_time >= 30):
            st.session_state[f"truck_{i}_status"] = "Reached NGO Destination"
            st.rerun()


# ==========================================
# 3. CORE MATHEMATICAL LOGIC FUNCTIONS
# ==========================================
def calculate_availability(produced, consumed):
    """Calculate remaining food."""
    return min(max(0, produced - consumed), 60)  # Cap at 60kg for truck limit


def calculate_trucks_needed(available_food, food_per_truck=20):
    """Calculate dynamic truck number based on leftover food."""
    if available_food <= 0:
        return 0
    return (available_food + food_per_truck - 1) // food_per_truck


# ==========================================
# 4. INTERACTION LOGIC (PROCESS BEFORE DRAWING)
# ==========================================
if "custom_prod_input" not in st.session_state:
    st.session_state.custom_prod_input = 0
if "custom_cons_input" not in st.session_state:
    st.session_state.custom_cons_input = 0


# ==========================================
# 5. UI DRAWING LAYOUT (SIDEBAR SECTIONS)
# ==========================================
st.title("Food Waste Reduction Platform")

st.sidebar.header("Operations Control Panel")

# A. Manual Override Form
with st.sidebar.form("override_form"):
    st.write("Manual Override Options")
    custom_prod = st.number_input(
        "Custom Food Produced (kg):", min_value=0, step=1
    )
    custom_cons = st.number_input(
        "Custom Food Consumed (kg):", min_value=0, step=1
    )
    submit_custom = st.form_submit_button("Apply Custom Input")

if submit_custom:
    if custom_prod > 0:
        if custom_cons > custom_prod:
            st.sidebar.error("Consumed cannot be more than produced!")
        else:
            st.session_state.food_produced = custom_prod
            st.session_state.food_consumed = custom_cons
            st.rerun()
    else:
        st.sidebar.warning("Enter production > 0 to override.")

# Calculate metrics to know how many buttons to show
available = calculate_availability(
    st.session_state.food_produced, st.session_state.food_consumed
)
trucks = calculate_trucks_needed(available)

st.sidebar.write("---")
st.sidebar.write("**Fleet Action Controls**")

# B. Dynamic Fleet Controls with 5-Second Cooldown Enforcement
for t_id in range(1, 4):
    if trucks >= t_id if t_id < 3 else trucks == 3:
        st.sidebar.markdown(f"### 🚛 Truck {t_id}")
        col1, col2 = st.sidebar.columns(2)

        with col1:
            if st.button(f"Dispatch T{t_id}", key=f"disp_t{t_id}"):
                st.session_state[f"truck_{t_id}_status"] = "In Transport"
                st.session_state[f"truck_{t_id}_dispatch_time"] = time.time()
                st.rerun()

        with col2:
            if st.button(f"Deliver T{t_id}", key=f"del_t{t_id}"):
                if st.session_state[f"truck_{t_id}_status"] == "In Transport":
                    elapsed = (
                        time.time()
                        - st.session_state[f"truck_{t_id}_dispatch_time"]
                    )
                    if elapsed < 5:
                        st.sidebar.error(
                            f"⚠️ Error: Truck {t_id} cannot deliver within 5s of dispatch!"
                        )
                    else:
                        st.session_state[f"truck_{t_id}_status"] = (
                            "Reached NGO Destination"
                        )
                        st.rerun()
                elif (
                    st.session_state[f"truck_{t_id}_status"]
                    == "Ready at Restaurant"
                ):
                    st.sidebar.warning(f"Truck {t_id} must be dispatched first!")

if trucks == 0:
    st.sidebar.info("No logistics actions required for 0 trucks.")

st.sidebar.write("---")

# C. Global Reset Button
if st.sidebar.button("⚠️ Reset: Change Day"):
    st.session_state.food_produced = random.randint(50, 150)  # nosec
    st.session_state.food_consumed = random.randint(  # nosec
        10, st.session_state.food_produced
    )
    # Reset all fleet positions and timestamps
    for i in range(1, 4):
        st.session_state[f"truck_{i}_status"] = "Ready at Restaurant"
        st.session_state[f"truck_{i}_dispatch_time"] = None
    st.rerun()


# ==========================================
# 6. MAIN DASHBOARD DISPLAY
# ==========================================
st.subheader("Daily Logistics Console")
st.text(f"Food Produced: {st.session_state.food_produced} kg")
st.text(f"Food Consumed: {st.session_state.food_consumed} kg")
st.metric(label="Available Food Remaining", value=f"{available} kg")
st.metric(
    label="Trucks Required Today (20 kg per truck, Max 3 Trucks)", value=trucks
)

st.write("---")

st.subheader("Food Status Tracker")

# Display statuses using clean blue highlight layouts (st.info)
if trucks >= 1:
    st.info(f"Truck 1 Status: {st.session_state.truck_1_status}")
if trucks >= 2:
    st.info(f"Truck 2 Status: {st.session_state.truck_2_status}")
if trucks == 3:
    st.info(f"Truck 3 Status: {st.session_state.truck_3_status}")
if trucks == 0:
    st.info("Status: No active food shipments today.")
