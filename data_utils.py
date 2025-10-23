import pandas as pd
import os

# Configuration Constants
SAMPLE_SIZE = 50
RANDOM_STATE = 42

RAW_DATA_FILE = 'Womens Clothing E-Commerce Reviews.csv'

def load_and_preprocess_data():
    """
    Loads the raw feedback data, cleans it, and returns a fixed-size sample for analysis.
    """
    if not os.path.exists(RAW_DATA_FILE):
        print(f"Error: Data file not found at {RAW_DATA_FILE}. Please check the file name or path.")
        return pd.DataFrame()

    df = pd.read_csv(RAW_DATA_FILE)

    # 1. Basic Cleaning: Remove rows where the main text is missing
    df_clean = df.dropna(subset=['Review Text']).copy()

    # 2. Filter out very short, non-meaningful reviews (less than 10 words)
    df_clean['text_length'] = df_clean['Review Text'].apply(lambda x: len(str(x).split()))
    df_final = df_clean[df_clean['text_length'] >= 10]

    # 3. Take a fixed sample
    if len(df_final) < SAMPLE_SIZE:
        print(f"Warning: Only {len(df_final)} reviews available.")
        df_sample = df_final.reset_index(drop=True)
    else:
        df_sample = df_final.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE).reset_index(drop=True)

    print(f"Data prepared successfully. Analyzing {len(df_sample)} reviews.")
    return df_sample

if __name__ == '__main__':
    # TEST: Run this block directly to confirm data loading
    sample_df = load_and_preprocess_data()
    if not sample_df.empty:
        print("\nTest Run: Sample Data Head")
        print(sample_df[['Review Text']].head())