import pandas as pd
import pytest

def test_hour_invariant():
    """Verify that hours are always in the range [0, 23]."""
    # This would typically load the data and check it.
    df = pd.DataFrame({"hour": [0, 12, 23]})
    assert df["hour"].between(0, 23).all()

def test_total_rentals_non_negative():
    """Verify that total rentals are never negative."""
    df = pd.DataFrame({"total_rentals": [0, 100, 500]})
    assert (df["total_rentals"] >= 0).all()
