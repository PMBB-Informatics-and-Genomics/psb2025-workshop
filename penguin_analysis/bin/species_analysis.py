#!/usr/bin/env python3
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze penguin species')
    parser.add_argument('-i', '--input_file', help='Input CSV file path')
    parser.add_argument('-s', '--species', help='Species to analyze')
    # parser.add_argument('-o', '--output_dir', help='Output directory for results')
    return parser.parse_args()

def load_and_filter_data(file_path, species):
    df = pd.read_csv(file_path)
    return df[df['species'] == species]

def calculate_basic_stats(df):
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    stats_df = df[numeric_cols].agg(['mean', 'std', 'min', 'max'])
    return stats_df

def analyze_sexual_dimorphism(df):
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    dimorphism_stats = {}
    
    for col in numeric_cols:
        male_data = df[df['sex'] == 'MALE'][col]
        female_data = df[df['sex'] == 'FEMALE'][col]
        
        t_stat, p_value = stats.ttest_ind(male_data, female_data)
        effect_size = (male_data.mean() - female_data.mean()) / np.sqrt((male_data.var() + female_data.var()) / 2)
        
        dimorphism_stats[col] = {
            't_statistic': t_stat,
            'p_value': p_value,
            'effect_size': effect_size
        }
    
    return pd.DataFrame(dimorphism_stats)

def create_morphological_plots(df, species):
    # Distribution plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Morphological Distributions - {species}')
    
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    for ax, col in zip(axes.flat, numeric_cols):
        sns.boxplot(data=df, x='sex', y=col, ax=ax)
        ax.set_title(col)
    
    plt.tight_layout()
    plt.savefig(f'{species}_distributions.png')
    plt.close()
    
    # Correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
    plt.title(f'Feature Correlations - {species}')
    plt.savefig(f'{species}_correlations.png')
    plt.close()

def main():
    args = parse_args()
    
    # Load and process data
    df = load_and_filter_data(args.input_file, args.species)
    
    # Calculate statistics
    basic_stats = calculate_basic_stats(df)
    dimorphism_stats = analyze_sexual_dimorphism(df)
    
    # Generate plots
    create_morphological_plots(df, args.species)
    
    # Save results
    basic_stats.to_csv(f'{args.species}_basic_stats.csv')
    dimorphism_stats.to_csv(f'{args.species}_dimorphism_stats.csv')
    
    print(f"Analysis completed for {args.species}")
    # print(f"Results saved in {args.output_dir}")

if __name__ == "__main__":
    main()
