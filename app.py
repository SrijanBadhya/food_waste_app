'''
MODULE DOCSTRING:
This Streamlit app simulates a food waste reduction platform for restaurants. 
'''

import random
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

# Track the independent status of each of the 3 possible trucks
if "truck_1_status" not in st.session_state:
    st.session_state.truck_1_status = "Ready at Restaurant"
if "truck_2_status" not in st.session_state:
    st.session_state.truck_2_status = "Ready at Restaurant"
if "truck_3_status" not in st.session_state:
    st.session_state.truck_3_status = "Ready at Restaurant"


# ==========================================
# 2. CORE MATHEMATICAL LOGIC FUNCTIONS
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
# 3. INTERACTION LOGIC (PROCESS BEFORE DRAWING)
# ==========================================
if "custom_prod_input" not in st.session_state:
    st.session_state.custom_prod_input = 0
if "custom_cons_input" not in st.session_state:
    st.session_state.custom_cons_input = 0


# ==========================================
# 4. UI DRAWING LAYOUT (SIDEBAR SECTIONS)
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

# B. Dynamic Vanishing/Appearance of Individual Truck Controls
if trucks >= 1:
    st.sidebar.markdown("### 🚛 Truck 1")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Dispatch T1", key="disp_t1"):
            st.session_state.truck_1_status = "In Transport"
            st.rerun()
    with col2:
        if st.button("Deliver T1", key="del_t1"):
            st.session_state.truck_1_status = "Reached NGO Destination"
            st.rerun()

if trucks >= 2:
    st.sidebar.markdown("### 🚛 Truck 2")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Dispatch T2", key="disp_t2"):
            st.session_state.truck_2_status = "In Transport"
            st.rerun()
    with col2:
        if st.button("Deliver T2", key="del_t2"):
            st.session_state.truck_2_status = "Reached NGO Destination"
            st.rerun()

if trucks == 3:
    st.sidebar.markdown("### 🚛 Truck 3")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Dispatch T3", key="disp_t3"):
            st.session_state.truck_3_status = "In Transport"
            st.rerun()
    with col2:
        if st.button("Deliver T3", key="del_t3"):
            st.session_state.truck_3_status = "Reached NGO Destination"
            st.rerun()

if trucks == 0:
    st.sidebar.info("No logistics actions required for 0 trucks.")

st.sidebar.write("---")

# C. Global Reset Button
if st.sidebar.button("⚠️ Reset: Change Day"):
    st.session_state.food_produced = random.randint(50, 150)  # nosec
    st.session_state.food_consumed = random.randint(  # nosec
        10, st.session_state.food_produced
    )
    # Reset all fleet positions back to baseline
    st.session_state.truck_1_status = "Ready at Restaurant"
    st.session_state.truck_2_status = "Ready at Restaurant"
    st.session_state.truck_3_status = "Ready at Restaurant"
    st.rerun()


# ==========================================
# 5. MAIN DASHBOARD DISPLAY
# ==========================================
st.subheader("Daily Logistics Console")
st.text(f"Food Produced: {st.session_state.food_produced} kg")
st.text(f"Food Consumed: {st.session_state.food_consumed} kg")
st.metric(label="Available Food Remaining", value=f"{available} kg")
st.metric(label="Trucks Required Today (20 kg per truck, Max 3 Trucks)", value=trucks)

st.write("---")

st.subheader("Food Status Tracker")

# Display statuses conditionally based on fleet activation
if trucks >= 1:
    st.text(f"Truck 1 Status: {st.session_state.truck_1_status}")
if trucks >= 2:
    st.text(f"Truck 2 Status: {st.session_state.truck_2_status}")
if trucks == 3:
    st.text(f"Truck 3 Status: {st.session_state.truck_3_status}")
if trucks == 0:
    st.info("Status: No active food shipments today.")