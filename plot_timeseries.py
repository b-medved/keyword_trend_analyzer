#!/usr/bin/env python3
"""
Plot Time Series - A script to plot time series data from raw_timeseries.csv using matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import argparse

def plot_timeseries(input_file: str = 'raw_timeseries.csv', keyword: str = None):
    """Plot the time series data for a keyword from the CSV file, filtered since 2022 and grouped by month (median)."""
    data = pd.read_csv(input_file)
    data['date'] = pd.to_datetime(data['date'])
    
    # Get the keyword column name (it's the first column that's not 'date' or 'isPartial')
    if keyword is None:
        keyword = [col for col in data.columns if col not in ['date', 'isPartial']][0]
    
    # Filter data since 2022
    data = data[data['date'] >= '2022-01-01']
    
    # Group by month and calculate median
    data['month'] = data['date'].dt.to_period('M')
    monthly_median = data.groupby('month')[keyword].median().reset_index()
    monthly_median['month'] = monthly_median['month'].dt.to_timestamp()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_median['month'], monthly_median[keyword], marker='o', label=f'{keyword} (monthly median)')
    plt.title(f'Monthly Median Time Series for {keyword} (Since 2022)')
    plt.xlabel('Month')
    plt.ylabel('Interest (Median)')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    output_file = f'timeseries_{keyword.replace(" ", "_")}.png'
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Plot time series data from raw_timeseries.csv')
    parser.add_argument('--input', '-i', default='raw_timeseries.csv', 
                      help='Input CSV file containing time series data (default: raw_timeseries.csv)')
    parser.add_argument('--keyword', '-k', help='Keyword to plot (default: first non-date column in the CSV)')
    args = parser.parse_args()
    
    plot_timeseries(args.input, args.keyword)

if __name__ == "__main__":
    main() 