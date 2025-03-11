import sys
import os
import pandas as pd
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from feature_engineering import (
    create_aggregate_features,
    classify_users_by_rfms,
    calculate_woe_and_bin_features,
    visualize_rfms_space
)

def mock_transaction_data():
    return pd.DataFrame({
        'CustomerId': [1, 1, 2, 2, 3, 3, 3],
        'TransactionStartTime': pd.date_range(start='2023-01-01', periods=7, freq='D'),
        'TransactionId': range(7),
        'Amount': [100, -50, 200, -100, 300, -150, 50]
    })

def test_create_aggregate_features():
    df = mock_transaction_data()
    df_agg = create_aggregate_features(df)
    
    assert 'CustomerId' in df_agg.columns
    assert 'Recency' in df_agg.columns
    assert 'Frequency' in df_agg.columns
    assert 'Monetary' in df_agg.columns
    assert df_agg.shape[0] == df['CustomerId'].nunique()

def test_classify_users_by_rfms():
    df = mock_transaction_data()
    df_agg = create_aggregate_features(df)
    r_threshold, f_threshold, m_threshold, dc_threshold, tv_threshold = visualize_rfms_space(df_agg)
    df_classified = classify_users_by_rfms(df_agg, r_threshold, f_threshold, m_threshold, dc_threshold, tv_threshold)
    
    assert 'Classification' in df_classified.columns
    assert 'is_high_risk' in df_classified.columns
    assert df_classified['is_high_risk'].isin([0, 1]).all()

def test_calculate_woe_and_bin_features():
    df = mock_transaction_data()
    df_agg = create_aggregate_features(df)
    df_agg['is_high_risk'] = np.random.randint(0, 2, size=len(df_agg))
    df_woe = calculate_woe_and_bin_features(df_agg, ['Monetary', 'Frequency'], 'is_high_risk')
    
    assert 'Monetary_binned_WoE' in df_woe.columns
    assert 'Frequency_binned_WoE' in df_woe.columns
    assert not df_woe[['Monetary_binned_WoE', 'Frequency_binned_WoE']].isna().any().any()

if __name__ == "__main__":
    pytest.main()
