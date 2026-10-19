import pandas as pd
import pytest
from analytics import Inventory


CSV_PATH = "data/inventory_data.csv" 

@pytest.fixture
def df():
    return pd.read_csv(CSV_PATH)

@pytest.fixture
def inv():
    return Inventory(CSV_PATH)

def test_expired_count_matches_pandas(df, inv):
    # A product is expired if DAYS_TO_EXPIRY is less than 0
    expected = len(df[df['DAYS_TO_EXPIRY'] < 0])
    assert inv.metrics['expired_count'] == expected

def test_expired_count_canary(inv):
    
    assert inv.metrics['expired_count'] == 1514

def test_total_inventory_value_matches_pandas(df, inv):
    # Value = ACTUAL_QTY * UNIT_PRICE_AED
    expected = (df['ACTUAL_QTY'] * df['UNIT_PRICE_AED']).sum()
   
    assert inv.metrics['total_inv_val'] == pytest.approx(expected)

def test_urgent_brands_matches_pandas(df, inv):

    urgent_df = df[(df['DAYS_TO_EXPIRY'] >= 0) & (df['DAYS_TO_EXPIRY'] <= 30)]
    expected_count = len(urgent_df['BRAND'].unique())
    assert len(inv.metrics['urgent_brands']) == expected_count