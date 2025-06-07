#!/usr/bin/env python3
"""
Time Series Puller - A script to pull historical time series data for a single keyword using Google Trends API
"""

import argparse
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime

def pull_timeseries(keyword: str, geo: str = 'US', output_file: str = 'raw_timeseries.csv', since: str = '2022-01-01'):
    """Pull historical time series data for a single keyword with weekly granularity since a given date."""
    print(f"Pulling historical time series for: {keyword} since {since}")
    pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=2, backoff_factor=0.1)
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        timeframe = f"{since} {today}"
        pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
        data = pytrends.interest_over_time()
        if not data.empty:
            data.to_csv(output_file)
            print(f"Raw time series data saved to {output_file}")
            print(data)
        else:
            print("No data returned for this keyword.")
    except Exception as e:
        print(f"Error pulling time series for {keyword}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Pull historical time series data for a single keyword')
    parser.add_argument('keyword', help='The keyword to pull time series data for')
    parser.add_argument('--geo', '-g', default='US', help='Geographic region for analysis (default: US)')
    parser.add_argument('--output', '-o', default='raw_timeseries.csv', help='Output CSV file for results (default: raw_timeseries.csv)')
    parser.add_argument('--since', default='2022-01-01', help='Start date for data collection (default: 2022-01-01)')
    args = parser.parse_args()

    pull_timeseries(args.keyword, args.geo, args.output, args.since)

if __name__ == "__main__":
    main() 