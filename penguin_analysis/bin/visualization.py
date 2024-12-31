#!/usr/bin/env python3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Create penguin visualizations')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('output_dir', help='Output directory for visualizations')
    return parser.parse_args()

def create_species_comparison(df, output_dir):
    # Create faceted boxplots
    fig = plt.figure(figsize=(15, 10))
    measurements = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    for idx, measure in enumerate(measurements, 1):
        plt.subplot(2, 2, idx)
        sns.boxplot(data=df, x='species', y=measure, hue='sex')
        plt.xticks(rotation=45)
        plt.title(f'{measure} by Species and Sex')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/species_comparison_boxplots.png', dpi=300)
    plt.close()

def create_interactive_scatter(df, output_dir):
    # Interactive scatter plot with Plotly
    fig = px.scatter(df, 
                    x='bill_length_mm', 
                    y='bill_depth_mm',
                    color='species',
                    symbol='sex',
                    size='body_mass_g',
                    hover_data=['flipper_length_mm'],
                    title='Bill Measurements by Species')
    
    fig.write_html(f'{output_dir}/interactive_scatter.html')

def create_correlation_heatmap(df, output_dir):
    # Correlation heatmap
    numeric_cols = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    corr = df[numeric_cols].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Penguin Measurements')
    plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_density_plots(df, output_dir):
    # Kernel Density Estimation plots
    fig = plt.figure(figsize=(15, 10))
    measurements = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    
    for idx, measure in enumerate(measurements, 1):
        plt.subplot(2, 2, idx)
        for species in df['species'].unique():
            subset = df[df['species'] == species]
            sns.kdeplot(data=subset, x=measure, label=species)
        plt.title(f'{measure} Distribution')
        plt.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/density_plots.png', dpi=300)
    plt.close()

def create_pair_plot(df, output_dir):
    # Pair plot for all numeric variables
    sns.pairplot(df, hue='species', diag_kind='kde')
    plt.savefig(f'{output_dir}/pair_plot.png', dpi=300)
    plt.close()

def create_island_distribution(df, output_dir):
    # Stacked bar chart of species distribution by island
    plt.figure(figsize=(10, 6))
    species_by_island = pd.crosstab(df['island'], df['species'])
    species_by_island.plot(kind='bar', stacked=True)
    plt.title('Species Distribution by Island')
    plt.xlabel('Island')
    plt.ylabel('Count')
    plt.legend(title='Species')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/island_distribution.png', dpi=300)
    plt.close()

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data
    df = pd.read_csv(args.input_file)
    
    # Create visualizations
    create_species_comparison(df, args.output_dir)
    create_interactive_scatter(df, args.output_dir)
    create_correlation_heatmap(df, args.output_dir)
    create_density_plots(df, args.output_dir)
    create_pair_plot(df, args.output_dir)
    create_island_distribution(df, args.output_dir)
    
    print(f"Visualizations saved to {args.output_dir}")

if __name__ == "__main__":
    main()
