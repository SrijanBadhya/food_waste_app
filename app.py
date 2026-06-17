# pylint: disable=no-member, invalid-name
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
if "food_status" not in st.session_state:
    st.session_state.food_status = "At Restaurant"


# ==========================================
# 2. CORE MATHEMATICAL LOGIC FUNCTIONS
# ==========================================
def calculate_availability(produced, consumed):
    """Calculate remaining food."""
    return max(0, produced - consumed)


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

# Setup Sidebar Header
st.sidebar.header("Operations Control Panel")

# A. Form displays first at the top of the sidebar
with st.sidebar.form("override_form"):
    st.write("Manual Override Options")
    custom_prod = st.number_input(
        "Custom Food Produced (kg):", min_value=0, step=1
    )
    custom_cons = st.number_input(
        "Custom Food Consumed (kg):", min_value=0, step=1
    )
    submit_custom = st.form_submit_button("Apply Custom Input")

# Process custom input immediately if submitted
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

st.sidebar.write("---")
st.sidebar.write("Action Controls")

# B. Action buttons display cleanly below the form section
if st.sidebar.button("🚚 Dispatch: Transfer to Truck"):
    st.session_state.food_status = "In Transport"
    st.rerun()

if st.sidebar.button("📍 Delivery: Transfer to Destination"):
    st.session_state.food_status = "Reached NGO Destination"
    st.rerun()

st.sidebar.write("---")

if st.sidebar.button("⚠️ Reset: Change Day"):
    st.session_state.food_produced = random.randint(50, 150)  # nosec
    st.session_state.food_consumed = random.randint(  # nosec
        10, st.session_state.food_produced
    )
    st.session_state.food_status = "At Restaurant"
    st.rerun()


# ==========================================
# 5. MAIN DASHBOARD DISPLAY
# ==========================================
st.subheader("Daily Logistics Console")
st.text(f"Food Produced: {st.session_state.food_produced} kg")
st.text(f"Food Consumed: {st.session_state.food_consumed} kg")

available = calculate_availability(
    st.session_state.food_produced, st.session_state.food_consumed
)
st.metric(label="Available Food Remaining", value=f"{available} kg")

trucks = calculate_trucks_needed(available)
st.metric(label="Trucks Required Today (20 kg capacity each)", value=trucks)

st.write("---")

st.subheader("Food Status Tracker")
st.info(f"Current Status: {st.session_state.food_status}")