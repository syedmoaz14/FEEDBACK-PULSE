# main.py

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

    # 1. Load and prepare the sample data
    df_sample = load_and_preprocess_data()
    if df_sample.empty:
        print("Pipeline aborted: Data loading failed.")
        return

    print(f"Processing {len(df_sample)} reviews. This may take a few minutes...")

    results_list = []

    # --- P3.3: Implement Batch Processing Loop ---
    for index, row in df_sample.iterrows():
        review_text = row['Review Text']

        analysis = call_llm_analysis(review_text)

        if analysis:
            # Add the original review's index and text to the result dictionary
            analysis['original_index'] = index
            results_list.append(analysis)

        # Rate Limiting: Add a small delay
        time.sleep(1)

        if (index + 1) % 10 == 0:
            print(f"-> Processed {index + 1} of {len(df_sample)} reviews...")

    print("--- LLM Analysis Complete ---")

    # --- P3.4 & P3.5: Process and Merge Results ---
    if not results_list:
        print("No successful LLM results were returned.")
        return

    df_results = pd.DataFrame(results_list)

    df_sample = df_sample.set_index(df_sample.index)

    # Merge based on original index
    df_final_analysis = pd.merge(
        df_sample,
        df_results,
        left_index=True,
        right_on='original_index',
        how='left'
    ).drop(columns=['original_index']).fillna({'sentiment': 'UNPROCESSED', 'topic': 'N/A', 'action_item': 'N/A'})

    print("\n--- Final Data Compilation Complete ---")

    # Save the master analysis file
    df_final_analysis.to_csv('master_analysis_data.csv', index=False)
    print("\nMaster analysis data saved to 'master_analysis_data.csv'.")

    return df_final_analysis


if __name__ == '__main__':
    run_analysis_pipeline()