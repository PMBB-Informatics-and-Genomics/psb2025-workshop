#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Clean Palmer Penguins dataset')
    parser.add_argument('-i', '--input_file', help='Input CSV file path')
    # parser.add_argument('-o', '--output_file', help='Output CSV file path')
    return parser.parse_args()

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_column_names(df):
    return df.rename(columns=lambda x: x.lower().replace(' ', '_'))

def remove_missing_values(df):
    return df.dropna()

def normalize_numeric_features(df):
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def validate_data(df):
    # Check for valid ranges
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    for col in numeric_cols:
        df = df[df[col].between(df[col].quantile(0.01), df[col].quantile(0.99))]
    
    # Validate species names
    valid_species = ['Adelie', 'Gentoo', 'Chinstrap']
    df = df[df['species'].isin(valid_species)]
    
    return df

def add_derived_features(df):
    # Add bill ratio feature
    df['bill_ratio'] = df['bill_length_mm'] / df['bill_depth_mm']
    
    # Add size category
    df['size_category'] = pd.qcut(df['body_mass_g'], q=3, labels=['small', 'medium', 'large'])
    
    return df

def main():
    args = parse_args()
    
    # Load and process data
    df = load_data(args.input_file)
    df = clean_column_names(df)
    df = remove_missing_values(df)
    df = validate_data(df)
    df = normalize_numeric_features(df)
    df = add_derived_features(df)
    
    # Save cleaned data
    output_file = 'penguins_cleaned.csv'
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")
    print(f"Shape of cleaned dataset: {df.shape}")

if __name__ == "__main__":
    main()
