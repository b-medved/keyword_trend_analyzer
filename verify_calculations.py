#!/usr/bin/env python3
"""
Verify Calculations - Compare raw time series data with aggregated results
"""

import pandas as pd
import argparse

def verify_calculations(raw_file: str, combined_file: str, keyword: str):
    """Verify calculations by comparing raw data with aggregated results."""
    # Read the files
    raw_data = pd.read_csv(raw_file)
    combined_data = pd.read_csv(combined_file)
    
    # Convert date to datetime
    raw_data['date'] = pd.to_datetime(raw_data['date'])
    
    # Calculate yearly medians from raw data
    raw_data['year'] = raw_data['date'].dt.year
    yearly_medians = raw_data.groupby('year')[keyword].median().reset_index()
    
    # Get the combined results for the keyword
    keyword_results = combined_data[combined_data['Keyword'] == keyword].iloc[0]
    
    print(f"\nVerification for keyword: {keyword}")
    print("\nRaw Data Yearly Medians:")
    print(yearly_medians)
    
    print("\nCombined Results:")
    for year in range(2021, 2026):
        if str(year) in keyword_results:
            print(f"{year}: {keyword_results[str(year)]}")
    
    # Compare the values
    print("\nComparison:")
    for _, row in yearly_medians.iterrows():
        year = int(row['year'])  # Convert to int
        raw_median = row[keyword]
        combined_value = keyword_results[str(year)]
        print(f"{year}: Raw Median = {raw_median:.2f}, Combined = {combined_value:.2f}")

def main():
    parser = argparse.ArgumentParser(description='Verify calculations between raw and combined data')
    parser.add_argument('--raw', '-r', default='raw_timeseries.csv',
                      help='Raw time series data file (default: raw_timeseries.csv)')
    parser.add_argument('--combined', '-c', default='combined_results.csv',
                      help='Combined results file (default: combined_results.csv)')
    parser.add_argument('--keyword', '-k', required=True,
                      help='Keyword to verify')
    args = parser.parse_args()
    
    verify_calculations(args.raw, args.combined, args.keyword)

if __name__ == "__main__":
    main() 