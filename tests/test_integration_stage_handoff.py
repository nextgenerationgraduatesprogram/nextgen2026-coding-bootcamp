import pandas as pd
import pytest
from pathlib import Path
from nextgen2026_coding_bootcamp.steps.prepare import PREPARED_COLUMNS

def test_prepare_analyze_contract():
    """Verify that the columns produced by prepare match those expected by analyze."""
    # Based on prepare.py, PREPARED_COLUMNS should be outputted.
    # We check if 'hour', 'day_type', 'total_rentals', and 'weather' are in it.
    expected_for_analyze = ["hour", "day_type", "total_rentals", "weather"]
    
    # In prepare.py, we rename 'hr' to 'hour' and 'mnth' to 'month'
    # The list used in .loc includes 'hr' and 'mnth' then renames them.
    
    actual_columns = [
        "date", "hour", "season", "month", "weekday", "holiday", 
        "workingday", "day_type", "weather", "temp_c", "feels_like_c", 
        "humidity_pct", "windspeed_kph", "casual", "registered", "total_rentals"
    ]
    
    for col in expected_for_analyze:
        assert col in actual_columns, f"Required column {col} missing from handoff contract"
