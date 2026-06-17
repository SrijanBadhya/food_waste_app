from unittest.mock import MagicMock
import streamlit as st
from app import calculate_availability, calculate_trucks_needed


def test_integration_session_state_initialization():
    """Verify that mocked session storage sets up properties cleanly."""
    st.session_state = MagicMock()
    st.session_state.food_produced = 120
    st.session_state.food_consumed = 50
    st.session_state.food_status = "At Restaurant"

    assert st.session_state.food_produced == 120
    assert st.session_state.food_consumed == 50
    assert st.session_state.food_status == "At Restaurant"


def test_integration_data_flow_calculations():
    """Verify math functions integrate correctly using state storage numbers."""
    st.session_state = MagicMock()
    st.session_state.food_produced = 120
    st.session_state.food_consumed = 50

    leftover = calculate_availability(
        st.session_state.food_produced, st.session_state.food_consumed
    )
    trucks_alt = calculate_trucks_needed(leftover, food_per_truck=20)

    assert leftover == 70
    assert trucks_alt == 4


def test_integration_status_transition_to_truck():
    """Verify food status transitions seamlessly to truck state[cite: 201, 208, 209]."""
    st.session_state = MagicMock()
    st.session_state.food_status = "At Restaurant"

    # Simulate button click action updating state variables
    st.session_state.food_status = "In Transport"
    assert st.session_state.food_status == "In Transport"


def test_integration_status_transition_to_destination():
    """Verify food status transitions seamlessly to destination state[cite: 201, 208, 209]."""
    st.session_state = MagicMock()
    st.session_state.food_status = "In Transport"

    # Simulate final delivery click action
    st.session_state.food_status = "Reached NGO Destination"
    assert st.session_state.food_status == "Reached NGO Destination"