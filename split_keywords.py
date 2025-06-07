#!/usr/bin/env python3
"""
Split keywords into multiple chunks for parallel processing.
Each chunk will be saved as a separate CSV file.
"""

import argparse
import pandas as pd
import math
import os

def split_keywords(input_file: str, num_chunks: int, output_dir: str = 'keyword_chunks'):
    """
    Split keywords into multiple chunks and save as separate CSV files.
    
    Args:
        input_file (str): Path to input CSV file containing keywords
        num_chunks (int): Number of chunks to split the keywords into
        output_dir (str): Directory to save the chunk files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read keywords
    try:
        df = pd.read_csv(input_file)
        if 'Keyword' not in df.columns:
            raise ValueError("CSV file must contain a 'Keyword' column")
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
    
    # Calculate chunk size
    total_keywords = len(df)
    chunk_size = math.ceil(total_keywords / num_chunks)
    
    # Split and save chunks
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, total_keywords)
        
        # Get chunk of keywords
        chunk_df = df.iloc[start_idx:end_idx]
        
        # Save chunk to CSV
        output_file = os.path.join(output_dir, f'keywords_chunk_{i+1}.csv')
        chunk_df.to_csv(output_file, index=False)
        
        print(f"Created chunk {i+1}/{num_chunks}: {output_file} ({len(chunk_df)} keywords)")

def main():
    parser = argparse.ArgumentParser(description='Split keywords into chunks for parallel processing')
    parser.add_argument('--input', '-i', default='keywords.csv', 
                      help='Input CSV file containing keywords (default: keywords.csv)')
    parser.add_argument('--chunks', '-n', type=int, default=2,
                      help='Number of chunks to split into (default: 2)')
    parser.add_argument('--output-dir', '-o', default='keyword_chunks',
                      help='Directory to save chunk files (default: keyword_chunks)')
    
    args = parser.parse_args()
    
    split_keywords(args.input, args.chunks, args.output_dir)

if __name__ == "__main__":
    main() 