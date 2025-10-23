
import pandas as pd
from data_utils import load_and_preprocess_data
from llm_analyzer import call_llm_analysis
import time
import json


def run_analysis_pipeline():
    """
    Orchestrates the data loading, LLM analysis, and final data compilation.
    """
    print("--- Starting FeedbackPulse Analysis Pipeline ---")

    # 1. Load and prepare the sample data (P3.3 Setup)
    df_sample = load_and_preprocess_data()
    if df_sample.empty:
        print("Pipeline aborted: Data loading failed.")
        return

    print(f"Processing {len(df_sample)} reviews. This may take a few minutes...")

    # List to store all structured JSON results from the LLM
    results_list = []

    # --- P3.3: Implement Batch Processing Loop ---
    for index, row in df_sample.iterrows():
        review_text = row['Review Text']

        # Call the LLM analysis function
        analysis = call_llm_analysis(review_text)

        if analysis:
            # Add the original review's index and text to the result dictionary
            analysis['original_index'] = index
            analysis['Review Text'] = review_text
            results_list.append(analysis)

        # Rate Limiting: Add a small delay to respect API limits and manage costs
        time.sleep(1)  # Wait 1 second between requests

        # Progress tracking
        if (index + 1) % 10 == 0:
            print(f"-> Processed {index + 1} of {len(df_sample)} reviews...")

    print("--- LLM Analysis Complete ---")

    # --- P3.4 & P3.5: Process and Merge Results ---
    if not results_list:
        print("No successful LLM results were returned.")
        return

    # Convert the list of structured results into a DataFrame
    df_results = pd.DataFrame(results_list)

    # Merge the LLM results back into the original dataframe
    # (We use the original_index for a clean merge, though simple concatenation is also possible)

    # Drop the original 'Review Text' from df_sample to avoid duplication on merge
    # We use the index of the original df_sample rows
    df_sample = df_sample.set_index(df_sample.index)

    # Use a cleaner merge strategy based on the index we preserved
    df_final_analysis = pd.merge(
        df_sample,
        df_results.drop(columns=['Review Text']),  # Drop the duplicate text column from the results
        left_index=True,
        right_on='original_index',
        how='left'
    ).drop(columns=['original_index']).fillna({'sentiment': 'UNPROCESSED', 'topic': 'N/A', 'action_item': 'N/A'})

    print("\n--- Final Data Compilation Complete ---")
    print("Final Analysis Data Head (Showing new columns):")
    print(df_final_analysis[['Review Text', 'sentiment', 'topic', 'action_item']].head())

    # Save the master analysis file for the Streamlit app to use
    df_final_analysis.to_csv('master_analysis_data.csv', index=False)
    print("\nMaster analysis data saved to 'master_analysis_data.csv'.")

    return df_final_analysis


if __name__ == '__main__':
    run_analysis_pipeline()