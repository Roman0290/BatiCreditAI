# import unittest
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# from category_encoders.woe import WOEEncoder
# from sklearn.linear_model import LogisticRegression
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, r2_score
# from scripts.credit_risk_assessment import calculate_woe_rfms_score, credit_score_model, calculate_credit_score
# import io
# import contextlib

# class TestCreditRiskAssessment(unittest.TestCase):

#     def setUp(self):
#         # Sample data for testing
#         self.data = {
#             'AccountId': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
#             'TransactionId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#             'Amount': [100, 200, 150, 250, 300, 100, 400, 200, 500, 100],
#             'TransactionYear': [2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023, 2023],
#             'TransactionMonth': [1, 2, 1, 3, 2, 4, 3, 5, 4, 6],
#             'TransactionDay': [1, 15, 5, 20, 10, 25, 15, 30, 20, 1],
#             'CustomerId': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
#             'CurrencyCode': ['USD', 'USD', 'EUR', 'EUR', 'GBP', 'GBP', 'CAD', 'CAD', 'JPY', 'JPY'],
#             'CountryCode': ['US', 'US', 'FR', 'FR', 'UK', 'UK', 'CA', 'CA', 'JP', 'JP'],
#             'ProductId': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'],
#             'ProductCategory': ['Electronics', 'Electronics', 'Clothing', 'Clothing', 'Books', 'Books', 'Home', 'Home', 'Toys', 'Toys'],
#             'ChannelId': ['Online', 'Online', 'Store', 'Store', 'Online', 'Online', 'Store', 'Store', 'Online', 'Online'],
#             'Value': [100, 200, 150, 250, 300, 100, 400, 200, 500, 100],
#             'TransactionHour': [10, 12, 14, 16, 18, 20, 22, 0, 2, 4],
#             'PricingStrategy': ['Fixed', 'Fixed', 'Variable', 'Variable', 'Fixed', 'Fixed', 'Variable', 'Variable', 'Fixed', 'Fixed'],
#             'FraudResult': [0, 0, 0, 0, 1, 1, 0, 0, 1, 0],
#             'RFMS_score': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], # Dummy RFMS_score for calculate_credit_score
#             'RFMS_bin_woe': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], # Dummy RFMS_bin_woe for calculate_credit_score
#             'assessment_binary': [0,0,0,0,1,1,0,0,1,0] # Dummy assessment_binary for calculate_credit_score
#         }
#         self.df = pd.DataFrame(self.data)

#     def test_calculate_woe_rfms_score(self):
#         """Test the calculate_woe_rfms_score function."""
#         result_df = calculate_woe_rfms_score(self.df.copy())
#         self.assertIsInstance(result_df, pd.DataFrame)
#         self.assertIn('RFMS_Score', result_df.columns)
#         self.assertIn('Assessment_Binary', result_df.columns)
#         self.assertIn('RFMS_bin_woe', result_df.columns)
#         self.assertIn('default_rate_per_bin', result_df.columns)
#         self.assertIn('woe_per_bin', result_df.columns)
#         self.assertIn('Frequency', result_df.columns) #Ensure frequency is present

#         # Additional checks for RFMS calculation correctness
#         self.assertAlmostEqual(result_df['Recency'].mean(), 0.0, places=5)
#         self.assertAlmostEqual(result_df['Frequency'].mean(), 0.0, places=5)
#         self.assertAlmostEqual(result_df['Monetary'].mean(), 0.0, places=5)
#         self.assertAlmostEqual(result_df['StdDev'].mean(), 0.0, places=5)

#     def test_calculate_credit_score(self):
#         """Test the calculate_credit_score function."""
#         result_df = calculate_credit_score(self.df.copy())
#         self.assertIsInstance(result_df, pd.DataFrame)
#         self.assertIn('credit_score', result_df.columns)
#         self.assertIn('fico_credit_score', result_df.columns)

#         # Check if FICO score is within expected range
#         self.assertTrue(all(result_df['fico_credit_score'] >= 300))
#         self.assertTrue(all(result_df['fico_credit_score'] <= 850))

#     def test_credit_score_model(self):
#         """Test the credit_score_model function."""
#         rfms_df = calculate_woe_rfms_score(self.df.copy())
#         model, result_df = credit_score_model(rfms_df.copy())
#         self.assertIsInstance(model, LinearRegression)
#         self.assertIsInstance(result_df, pd.DataFrame)
#         self.assertIn('fico_credit_score', result_df.columns)
#         self.assertIn('RFMS_score', result_df.columns)
#         self.assertIn('RFMS_bin_woe', result_df.columns)

#         # Basic model evaluation test
#         X = result_df[['RFMS_score', 'RFMS_bin_woe']]
#         y = result_df['fico_credit_score']
#         y_pred = model.predict(X)
#         self.assertIsInstance(mean_squared_error(y, y_pred), float)
#         self.assertIsInstance(r2_score(y, y_pred), float)

#     def test_calculate_woe_rfms_score_print_output(self):
#         """Test if the print statements in calculate_woe_rfms_score produce output."""
#         captured_output = io.StringIO()
#         with contextlib.redirect_stdout(captured_output):
#             calculate_woe_rfms_score(self.df.copy())
#         output = captured_output.getvalue()
#         self.assertIn("Mean RFMS Score:", output)
#         self.assertIn("Median RFMS Score:", output)
#         self.assertIn("Standard Deviation of RFMS Scores:", output)