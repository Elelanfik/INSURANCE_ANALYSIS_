import pandas as pd
import sqlite3

def load_data(file_path):
    return pd.read_csv(file_path)
import pandas as pd

def load_and_save_txt(file_path, save_path, delimiter="|"):
    """
    Load a .txt file into a pandas DataFrame and save it as a .csv file.

    Args:
        file_path (str): Path to the .txt file.
        save_path (str): Path to save the .csv file.
        delimiter (str): Delimiter used in the .txt file (default is '|').

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    try:
        # Load the .txt file into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter)
        
        # Save the DataFrame as a .csv file
        df.to_csv(save_path, index=False)
        print(f"File saved successfully to {save_path}")
        
        return df
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
