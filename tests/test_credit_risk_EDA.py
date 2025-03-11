import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.credit_risk_EDA import CreditRiskEDA
import io
import contextlib

# Use Agg backend for headless testing
import matplotlib
matplotlib.use('Agg')

class TestCreditRiskEDA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data for the tests."""
        data = {
            'CustomerId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Amount': [200, 1500, 500, 1000, 1200, 300, 800, 1100, 600, 1400],
            'LastTransactionDate': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01', '2024-06-01', '2024-07-01', '2024-08-01', '2024-09-01', '2024-10-01']),
            'TransactionId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Gender': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
            'Category': ['A', 'B', 'A', 'C', 'B', 'C', 'A', 'B', 'C', 'A']
        }
        cls.df = pd.DataFrame(data)
        cls.eda = CreditRiskEDA(cls.df)

    def test_data_overview(self):
        """Test the data overview functionality."""
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            self.eda.data_overview()
        output = captured_output.getvalue()
        self.assertIn("Data Overview:", output)
        self.assertIn("Number of rows: 10", output)
        self.assertIn("Number of columns: 6", output)

    def test_summary_statistics(self):
        """Test summary statistics calculation."""
        summary_stats = self.eda.summary_statistics()
        self.assertEqual(summary_stats.shape[0], 3)
        self.assertIn('mean', summary_stats.columns)
        self.assertIn('skewness', summary_stats.columns)
        self.assertIn('kurtosis', summary_stats.columns)

    def test_plot_numerical_distribution(self):
        """Test numerical distribution plot functionality."""
        cols = ['Amount', 'TransactionId']
        try:
            self.eda.plot_numerical_distribution(cols)
        except Exception as e:
            self.fail(f"plot_numerical_distribution raised {e} unexpectedly!")

    def test_plot_skewness(self):
        """Test skewness plot."""
        try:
            self.eda.plot_skewness()
        except Exception as e:
            self.fail(f"plot_skewness raised {e} unexpectedly!")

    def test_plot_categorical_distribution(self):
        """Test categorical distribution plot."""
        try:
            self.eda.plot_categorical_distribution()
        except Exception as e:
            self.fail(f"plot_categorical_distribution raised {e} unexpectedly!")

    def test_correlation_analysis(self):
        """Test correlation analysis."""
        try:
            self.eda.correlation_analysis()
        except Exception as e:
            self.fail(f"correlation_analysis raised {e} unexpectedly!")

    def test_check_missing_values(self):
        """Test missing value detection."""
        captured_output = io.StringIO()
        with contextlib.redirect_stdout(captured_output):
            self.eda.check_missing_values()
        output = captured_output.getvalue()
        self.assertIn("Missing Values in Each Column:", output)

        try:
            self.eda.check_missing_values()
        except Exception as e:
            self.fail(f"check_missing_values raised {e} unexpectedly!")

    def test_detect_outliers(self):
        """Test outlier detection functionality."""
        cols = ['Amount', 'TransactionId']
        try:
            self.eda.detect_outliers(cols)
        except Exception as e:
            self.fail(f"detect_outliers raised {e} unexpectedly!")