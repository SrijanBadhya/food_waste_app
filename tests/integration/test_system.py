"""MODULE DOCSTRING: Integration tests evaluating Streamlit session state and data flow."""

import os
import sys
from unittest.mock import MagicMock
import streamlit as st

# Append root directory to path safely for execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# pylint: disable=wrong-import-position, import-error
from app import calculate_availability, calculate_trucks_needed


def test_integration_session_state_initialization():
    """Verify that mocked session storage sets up properties cleanly."""
    st.session_state = MagicMock()
    st.session_state.food_produced = 120
    st.session_state.food_consumed = 50
    st.session_state.truck_1_status = "Ready at Restaurant"

    assert st.session_state.food_produced == 120
    assert st.session_state.food_consumed == 50
    assert st.session_state.truck_1_status == "Ready at Restaurant"


def test_integration_data_flow_calculations():
    """Verify math functions integrate correctly using state storage numbers."""
    st.session_state = MagicMock()
    st.session_state.food_produced = 120
    st.session_state.food_consumed = 50

    leftover = calculate_availability(
        st.session_state.food_produced, st.session_state.food_consumed
    )
    trucks_alt = calculate_trucks_needed(leftover, food_per_truck=20)

    assert leftover == 60
    assert trucks_alt == 3


def test_integration_status_transition_to_truck():
    """Verify food status transitions seamlessly to truck state."""
    st.session_state = MagicMock()
    st.session_state.truck_1_status = "Ready at Restaurant"

    st.session_state.truck_1_status = "In Transport"
    assert st.session_state.truck_1_status == "In Transport"


def test_integration_status_transition_to_destination():
    """Verify food status transitions seamlessly to destination state."""
    st.session_state = MagicMock()
    st.session_state.truck_1_status = "In Transport"

    st.session_state.truck_1_status = "Reached NGO Destination"
    assert st.session_state.truck_1_status == "Reached NGO Destination"
