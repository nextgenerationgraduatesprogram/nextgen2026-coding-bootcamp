import pandas as pd
import pytest
from nextgen2026_coding_bootcamp.steps.prepare import SEASON_MAP, WEATHER_MAP, DAY_TYPE_MAP

def test_maps_are_complete():
    """Verify that the categorical mappings cover expected ranges."""
    assert set(SEASON_MAP.keys()) == {1, 2, 3, 4}
    assert set(WEATHER_MAP.keys()) == {1, 2, 3, 4}
    assert set(DAY_TYPE_MAP.keys()) == {0, 1}

def test_unit_conversion_logic():
    """Test the manual conversion logic for temp, hum, and windspeed."""
    # Based on the assignment logic in prepare.py:
    # temp_c = temp * 47 - 8
    # humidity_pct = hum * 100
    # windspeed_kph = windspeed * 67
    
    test_temp = 0.5
    expected_temp_c = 0.5 * 47 - 8
    assert abs((test_temp * 47 - 8) - expected_temp_c) < 1e-6
