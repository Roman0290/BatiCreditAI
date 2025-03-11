# Importing necessary libraries
import pandas as pd
import os


class DataLoader:
    """
    Class to load and save datasets from CSV or Parquet files.
    """
    @staticmethod
    def load_data(path):
        """
        Load the dataset from a CSV or Parquet file.

        Args:
            path (str): Path to the dataset file.

        Returns:
            pandas.DataFrame: The loaded dataset.
        """
        try:
            # Check if the file is a Parquet file
            if path.endswith('.parquet'):
                df = pd.read_parquet(path, engine='pyarrow')
            # Check if the file is a CSV file
            elif path.endswith('.csv'):
                df = pd.read_csv(path, low_memory=False)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV or Parquet file.")
            return df
        except FileNotFoundError as e:
            print(f"Error: {e}. The dataset file was not found.")
        except pd.errors.ParserError as e:
            print(f"Error: {e}. An error occurred while parsing the dataset.")
        except Exception as e:
            print(f"Error: {e}. An unknown error occurred while loading the dataset.")
        return None
   
    @staticmethod
    def save_data(df, output_folder, filename):
        """
        Save the cleaned dataset to a Parquet file.
        """
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, filename)
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"Dataset saved successfully at: {output_path}")
        return output_path

    


class DataCleaner:
    """
    Class to clean the dataset by handling missing values, outliers, and data type issues.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def identify_variable_types(self):
        """
        Identify categorical and numerical variables.

        Returns:
            tuple: Lists of categorical and numerical variable names.
        """
        categorical_vars = self.df.select_dtypes(include=['object']).columns.tolist()
        numerical_vars = self.df.select_dtypes(include=['int', 'float']).columns.tolist()
        return categorical_vars, numerical_vars

    def fill_missing_values(self, categorical_vars, numerical_vars):
        """
        Fill missing values for categorical and numerical variables.

        Args:
            categorical_vars (list): List of categorical variable names.
            numerical_vars (list): List of numerical variable names.

        Returns:
            pandas.DataFrame: DataFrame with missing values filled.
        """
        # Fill missing values for categorical variables with mode
        self.df[categorical_vars] = self.df[categorical_vars].fillna(self.df[categorical_vars].mode().iloc[0])
        
        # Fill missing values for numerical variables with mean
        self.df[numerical_vars] = self.df[numerical_vars].fillna(self.df[numerical_vars].mean())
        return self.df

    def handle_outliers(self, numerical_vars):
        """
        Handle outliers in numerical variables by capping them.

        Args:
            numerical_vars (list): List of numerical variable names.

        Returns:
            pandas.DataFrame: DataFrame with outliers removed or capped.
        """
        for col in numerical_vars:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
           
            # Cap the outliers to the lower and upper bounds
            self.df[col] = self.df[col].clip(lower=lower_bound, upper=upper_bound)
        return self.df

    def remove_constant_columns(self):
        """
        Remove columns that have no variation (constant columns).
        """
        constant_columns = [col for col in self.df.columns if self.df[col].nunique() == 1]
        self.df.drop(columns=constant_columns, inplace=True)
        return self.df

    def convert_to_datetime(self, date_columns):
        """
        Convert specified columns to datetime.

        Args:
            date_columns (list): List of date column names.

        Returns:
            pandas.DataFrame: DataFrame with datetime columns converted.
        """
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        return self.df