#!/usr/bin/env python3
"""
Keyword Trend Analyzer - A tool to analyze keyword trends using Google Trends API
"""

import os
import time
import argparse
from typing import Dict, List, Optional
import pandas as pd
from pytrends.request import TrendReq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class KeywordTrendAnalyzer:
    def __init__(self, hl: str = 'en-US', tz: int = 360, geo: str = 'US'):
        """Initialize the analyzer with language, timezone, and geographic settings."""
        self.pytrends = TrendReq(hl=hl, tz=tz, timeout=(10,25), retries=2, backoff_factor=0.1)
        self.geo = geo
        self.timeframes = {
            '1y': 'today 12-m',
            '3m': 'today 3-m'
        }

    def get_high_granularity_timeseries(self, keyword: str, timeframe: str = 'now 7-d', output_file: str = 'raw_timeseries.csv'):
        """Pull and save the highest granularity time series data for a keyword."""
        print(f"Pulling high granularity time series for: {keyword} (timeframe: {timeframe})")
        try:
            self.pytrends.build_payload([keyword], timeframe=timeframe, geo=self.geo)
            data = self.pytrends.interest_over_time()
            if not data.empty:
                data.to_csv(output_file)
                print(f"Raw time series data saved to {output_file}")
                print(data)
            else:
                print("No data returned for this keyword and timeframe.")
        except Exception as e:
            print(f"Error pulling time series for {keyword}: {str(e)}")

    def analyze_keywords(self, keywords_df: pd.DataFrame) -> pd.DataFrame:
        """Analyze trends for a list of keywords from a DataFrame."""
        results = []
        
        for _, row in keywords_df.iterrows():
            keyword = row['Keyword']
            print(f"Analyzing keyword: {keyword}")
            avg_data = self._get_average_data(keyword)
            
            # Calculate trends if we have enough data
            if avg_data.get('1y') and avg_data.get('3m'):
                trend = round(((avg_data['3m'] - avg_data['1y']) / avg_data['1y']) * 100, 1)
            else:
                trend = 'N/A'

            results.append({
                "Keyword": keyword,
                "1Y Avg": avg_data.get('1y'),
                "3M Avg": avg_data.get('3m'),
                "1Y → 3M % Change": f"{trend}%"
            })
            
            # Respect API rate limits with increased delay
            print("Waiting 65 seconds before next request...")
            time.sleep(65)  # Increased delay between requests

        return pd.DataFrame(results)

    def _get_average_data(self, keyword: str) -> Dict[str, Optional[float]]:
        """Get average data for a single keyword across different timeframes."""
        avg_data = {}
        
        for label, tf in self.timeframes.items():
            try:
                self.pytrends.build_payload([keyword], timeframe=tf, geo=self.geo)
                data = self.pytrends.interest_over_time()
                if not data.empty:
                    avg = data[keyword].mean()
                    avg_data[label] = round(avg, 2)
                else:
                    avg_data[label] = None
            except Exception as e:
                print(f"Error analyzing {keyword} for {label}: {str(e)}")
                avg_data[label] = None
                time.sleep(10)  # Additional delay after an error

        return avg_data

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze keyword trends using Google Trends API')
    parser.add_argument('--input', '-i', default='keywords.csv',
                      help='Input CSV file containing keywords (default: keywords.csv)')
    parser.add_argument('--output', '-o', default='keyword_trends_comparison.csv',
                      help='Output CSV file for results (default: keyword_trends_comparison.csv)')
    parser.add_argument('--geo', '-g', default='US',
                      help='Geographic region for analysis (default: US)')
    parser.add_argument('--raw', action='store_true', help='If set, pull and save high granularity time series for the first keyword only')
    
    args = parser.parse_args()

    # Read keywords from CSV
    try:
        keywords_df = pd.read_csv(args.input)
        if 'Keyword' not in keywords_df.columns:
            raise ValueError("CSV file must contain a 'Keyword' column")
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return

    # Initialize analyzer
    analyzer = KeywordTrendAnalyzer(geo=args.geo)
    
    if args.raw:
        # Pull high granularity time series for the first keyword
        first_keyword = keywords_df.iloc[0]['Keyword']
        analyzer.get_high_granularity_timeseries(first_keyword)
        return

    # Analyze keywords
    results_df = analyzer.analyze_keywords(keywords_df)
    
    # Display results
    print("\nResults:")
    print(results_df)
    
    # Save to CSV
    results_df.to_csv(args.output, index=False)
    print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main() 