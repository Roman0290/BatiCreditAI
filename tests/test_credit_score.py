import pytest
import pandas as pd
from scripts.credit_score import assign_credit_score  # Replace 'your_module' with the actual module name

def test_assign_credit_score():
    test_data = pd.DataFrame({
        'risk_probability': [0.0, 0.2, 0.5, 0.7, 0.9, 1.0]
    })

    expected_scores = [850, 740, 575, 465, 350, 300]  # Floor instead of round
    expected_ratings = ['Exceptional', 'Very Good', 'Fair', 'Poor', 'Poor', 'Poor']

    result_df = assign_credit_score(test_data)

    assert result_df['credit_score'].tolist() == expected_scores, f"Expected {expected_scores}, got {result_df['credit_score'].tolist()}"
    assert result_df['Rating'].tolist() == expected_ratings, f"Expected {expected_ratings}, got {result_df['Rating'].tolist()}"


if __name__ == "__main__":
    pytest.main()