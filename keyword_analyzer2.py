#!/usr/bin/env python3
"""
Keyword Trend Analyzer 2 - A tool to analyze keyword trends using Google Trends API, collecting data since 2022 and grouping by monthly median.
Supports batch processing of keywords to reduce total processing time.
"""

import os
import time
import argparse
from typing import Dict, List, Optional
import pandas as pd
from pytrends.request import TrendReq
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

class KeywordTrendAnalyzer2:
    def __init__(self, hl: str = 'en-US', tz: int = 360, geo: str = 'US'):
        """Initialize the analyzer with language, timezone, and geographic settings."""
        self.pytrends = TrendReq(hl=hl, tz=tz, timeout=(10,25), retries=2, backoff_factor=0.1)
        self.geo = geo

    def analyze_keyword_batch(self, keywords: List[str], timeframe: str) -> List[pd.DataFrame]:
        """Analyze a batch of up to 5 keywords simultaneously."""
        results = []
        try:
            # Build payload for the batch
            self.pytrends.build_payload(keywords, timeframe=timeframe, geo=self.geo)
            data = self.pytrends.interest_over_time()
            
            if not data.empty:
                # Process each keyword in the batch
                for keyword in keywords:
                    if keyword in data.columns:
                        # Group by month and calculate median
                        data['month'] = data.index.to_period('M')
                        monthly_median = data.groupby('month')[keyword].median().reset_index()
                        monthly_median['month'] = monthly_median['month'].dt.to_timestamp()
                        # Group by year and calculate median
                        monthly_median['year'] = monthly_median['month'].dt.year
                        yearly_median = monthly_median.groupby('year')[keyword].median().reset_index()
                        yearly_median = yearly_median.rename(columns={keyword: 'value'})
                        yearly_median['Keyword'] = keyword
                        results.append(yearly_median)
                    else:
                        print(f"No data returned for {keyword}.")
        except Exception as e:
            print(f"Error analyzing batch: {str(e)}")
        return results

    def analyze_keywords(self, keywords_df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
        """Analyze trends for a list of keywords from a DataFrame using batch processing."""
        results = []
        keywords = keywords_df['Keyword'].tolist()
        
        # Process keywords in batches of 5
        for i in range(0, len(keywords), 5):
            batch = keywords[i:i+5]
            print(f"\nAnalyzing batch of keywords: {batch}")
            batch_results = self.analyze_keyword_batch(batch, timeframe)
            results.extend(batch_results)
            
            # Respect API rate limits between batches
            if i + 5 < len(keywords):
                print("Waiting 65 seconds before next batch...")
                time.sleep(65)
        
        if results:
            combined_results = pd.concat(results, ignore_index=True)
            # Pivot the results to get columns: Keyword, 2021, 2022, 2023, 2024, 2025
            pivoted_results = combined_results.pivot(index='Keyword', columns='year', values='value').reset_index()
            return pivoted_results
        else:
            return pd.DataFrame(columns=['Keyword', '2021', '2022', '2023', '2024', '2025'])

def main():
    parser = argparse.ArgumentParser(description='Analyze keyword trends using Google Trends API with batch processing')
    parser.add_argument('--input', '-i', default='keywords.csv', help='Input CSV file containing keywords (default: keywords.csv)')
    parser.add_argument('--output', '-o', default='keyword_trends_yearly_median.csv', help='Output CSV file for results (default: keyword_trends_yearly_median.csv)')
    parser.add_argument('--geo', '-g', default='US', help='Geographic region for analysis (default: US)')
    parser.add_argument('--timeframe', '-t', default='2022-01-01 2025-06-01', 
                      help='Timeframe for analysis in format "YYYY-MM-DD YYYY-MM-DD" (default: 2022-01-01 2025-06-01)')
    args = parser.parse_args()

    try:
        keywords_df = pd.read_csv(args.input)
        if 'Keyword' not in keywords_df.columns:
            raise ValueError("CSV file must contain a 'Keyword' column")
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    analyzer = KeywordTrendAnalyzer2(geo=args.geo)
    results_df = analyzer.analyze_keywords(keywords_df, args.timeframe)
    print("\nResults:")
    print(results_df)
    results_df.to_csv(args.output, index=False)
    print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main() 