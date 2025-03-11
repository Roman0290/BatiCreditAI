import pytest
import pandas as pd
from unittest.mock import patch
from io import StringIO
import os
from scripts.data_preprocessor import DataLoader, DataCleaner


# Mock DataLoader test cases
@pytest.fixture
def mock_csv_data():
    # Create a mock CSV file in memory using StringIO
    data = StringIO("""
    CustomerId,TransactionStartTime,TransactionId,Amount
    1,2023-01-01,1,100
    2,2023-01-02,2,200
    3,2023-01-03,3,-50
    """)
    df = pd.read_csv(data)
    return df

def test_load_csv_data(mock_csv_data):
    # Mock the CSV loading function
    with patch("pandas.read_csv") as mock_read_csv:
        mock_read_csv.return_value = mock_csv_data
        df = DataLoader.load_data('test.csv')
        df.columns = df.columns.str.strip()  # Strip whitespace from column names
        assert df.shape == (3, 4)
        assert list(df.columns) == ['CustomerId', 'TransactionStartTime', 'TransactionId', 'Amount']

def test_load_invalid_file_format():
    # Test handling of invalid file format
    with patch("builtins.print") as mock_print:
        df = DataLoader.load_data('test.txt')
        assert df is None
        mock_print.assert_called_with("Error: Unsupported file format. Please provide a CSV or Parquet file.. An unknown error occurred while loading the dataset.")

def test_save_data(mock_csv_data):
    # Test saving a DataFrame to a parquet file
    with patch("os.makedirs") as mock_makedirs, patch("pandas.DataFrame.to_parquet") as mock_to_parquet:
        output_path = DataLoader.save_data(mock_csv_data, 'output', 'test_output.parquet')
        expected_output_path = os.path.join('output', 'test_output.parquet')  # Use os.path.join for cross-platform paths
        assert output_path == expected_output_path
        mock_makedirs.assert_called_with('output', exist_ok=True)
        mock_to_parquet.assert_called_with(expected_output_path, engine='pyarrow', index=False)


# Mock DataCleaner test cases
@pytest.fixture
def mock_clean_data():
    # Create a DataFrame for cleaning
    data = {
        'CustomerId': [1, 2, 3],
        'TransactionStartTime': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Amount': [100, 200, None],
        'Category': ['A', 'B', None],
    }
    df = pd.DataFrame(data)
    return df

def test_identify_variable_types(mock_clean_data):
    cleaner = DataCleaner(mock_clean_data)
    categorical_vars, numerical_vars = cleaner.identify_variable_types()
    assert sorted(categorical_vars) == sorted(['Category', 'TransactionStartTime'])
    assert sorted(numerical_vars) == sorted(['CustomerId', 'Amount'])

def test_handle_outliers_no_change(mock_clean_data):
    cleaner = DataCleaner(mock_clean_data)
    categorical_vars, numerical_vars = cleaner.identify_variable_types()

    # Create mock data without outliers (length of 3 matching the mock data)
    mock_clean_data['Amount'] = [100, 200, 300]
    cleaned_data = cleaner.handle_outliers(numerical_vars)

    # No outliers, so data should remain the same
    assert cleaned_data['Amount'].equals(mock_clean_data['Amount'])

def test_save_data_invalid_df():
    invalid_df = None  # Pass None as the DataFrame
    with pytest.raises(AttributeError):  # Should raise an error
        DataLoader.save_data(invalid_df, 'output', 'invalid_data.parquet')

def test_fill_missing_values_no_missing_data(mock_clean_data):
    no_missing_data = mock_clean_data.dropna()
    cleaner = DataCleaner(no_missing_data)
    categorical_vars, numerical_vars = cleaner.identify_variable_types()
    
    # No missing data, so it should return the same DataFrame
    cleaned_data = cleaner.fill_missing_values(categorical_vars, numerical_vars)
    assert cleaned_data.equals(no_missing_data)
