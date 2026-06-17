"""MODULE DOCSTRING: Unit tests evaluating core mathematical logic functions."""

import os
import sys

# Append root directory to path safely for execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# pylint: disable=wrong-import-position, import-error
from app import calculate_availability, calculate_trucks_needed


def test_availability_normal_subtraction():
    """Test standard food deduction calculation."""
    assert calculate_availability(100, 40) == 60


def test_availability_exact_match_zero():
    """Test that availability hits zero when food is fully consumed."""
    assert calculate_availability(50, 50) == 0


def test_trucks_needed_exact_division():
    """Test that trucks calculate evenly based on 20kg capacity."""
    assert calculate_trucks_needed(60, food_per_truck=20) == 3


def test_trucks_needed_empty_load():
    """Test that zero remaining food requires exactly zero trucks."""
    assert calculate_trucks_needed(0) == 0
