#!/usr/bin/env python3
"""
Combine results from multiple chunk files into a single CSV file.
This script will look for result files in the specified directory and combine them.
"""

import argparse
import pandas as pd
import os
import glob

def combine_results(input_dir: str, output_file: str, pattern: str = 'results_chunk_*.csv'):
    """
    Combine results from multiple chunk files into a single CSV file.
    
    Args:
        input_dir (str): Directory containing the chunk result files
        output_file (str): Path to save the combined results
        pattern (str): Pattern to match result files (default: 'results_chunk_*.csv')
    """
    try:
        # Find all result files matching the pattern
        result_files = glob.glob(os.path.join(input_dir, pattern))
        
        if not result_files:
            print(f"No result files found matching pattern '{pattern}' in {input_dir}")
            return
        
        # Read and combine all results
        results = []
        for file in sorted(result_files):
            try:
                df = pd.read_csv(file)
                results.append(df)
                print(f"Read results from {file} ({len(df)} keywords)")
            except Exception as e:
                print(f"Error reading {file}: {str(e)}")
        
        if results:
            # Combine all results
            combined_results = pd.concat(results, ignore_index=True)
            
            # Remove any duplicate keywords (in case of overlap)
            combined_results = combined_results.drop_duplicates(subset=['Keyword'])
            
            # Sort by keyword
            combined_results = combined_results.sort_values('Keyword')
            
            # Save combined results
            combined_results.to_csv(output_file, index=False)
            print(f"\nCombined {len(combined_results)} unique keywords into {output_file}")
        else:
            print("No results to combine")
            
    except Exception as e:
        print(f"Error combining results: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Combine results from multiple chunk files')
    parser.add_argument('--input-dir', '-i', default='.',
                      help='Directory containing result files (default: current directory)')
    parser.add_argument('--output', '-o', default='combined_results.csv',
                      help='Output file for combined results (default: combined_results.csv)')
    parser.add_argument('--pattern', '-p', default='results_chunk_*.csv',
                      help='Pattern to match result files (default: results_chunk_*.csv)')
    
    args = parser.parse_args()
    
    combine_results(args.input_dir, args.output, args.pattern)

if __name__ == "__main__":
    main() 