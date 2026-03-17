"""
Lab 2 — Learner Test File

Write your own pytest tests here. You must implement at least 3 test functions:
  - test_load_data_returns_dataframe
  - test_clean_data_no_nulls
  - test_add_features_creates_revenue

The autograder will run your tests as part of the CI check.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import numpy as np
import pytest
from pipeline import load_data, clean_data, add_features


# ─── Test 1 ───────────────────────────────────────────────────────────────────


def test_load_data_returns_dataframe():
    """load_data returns a DataFrame with expected columns."""
    import pandas as pd
    from pipeline import load_data
    
    df = load_data('data/sales_records.csv')
    
    # Verify that the result is DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Verify that the table contains rows
    assert len(df) > 0
    
    # Verify that the basic columns are present
    expected_columns = ['date', 'store_id', 'product_category', 'quantity', 'unit_price', 'payment_method']
    for col in expected_columns:
        assert col in df.columns


def test_clean_data_no_nulls():
    """After clean_data, quantity and unit_price have no NaN values."""
    import pandas as pd
    from pipeline import load_data, clean_data
    
    df = load_data('data/sales_records.csv')
    cleaned = clean_data(df)
    
    # Verify that there are no NaN values in quantity and unit_price
    assert cleaned['quantity'].isna().sum() == 0
    assert cleaned['unit_price'].isna().sum() == 0        


def test_add_features_creates_revenue():
    """add_features creates a 'revenue' column equal to quantity * unit_price."""
    import pandas as pd
    from pipeline import load_data, clean_data, add_features
    
    df = load_data('data/sales_records.csv')
    cleaned = clean_data(df)
    featured = add_features(cleaned)
    
    # Verify that the 'revenue' column exists
    assert 'revenue' in featured.columns
    
    # Verify that the values are correct
    expected_revenue = cleaned['quantity'] * cleaned['unit_price']
    pd.testing.assert_series_equal(featured['revenue'], expected_revenue, check_names=False)p