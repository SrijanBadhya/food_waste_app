from app import calculate_availability, calculate_trucks_needed


def test_math_logic():
    assert calculate_availability(100, 40) == 60
    assert calculate_availability(50, 50) == 0
    assert calculate_trucks_needed(60, food_per_truck=20) == 3
    assert calculate_trucks_needed(0) == 0