import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

def generate_seo_performance_plot():
    # Load the data
    df = pd.read_csv("sectionCdata/seo.csv")

    # Set position for each bar
    brands = df['Brand']
    x = np.arange(len(brands))  # Label locations
    width = 0.35  # Width of the bars

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, df['Domain Authority (DA)'], width, label='Domain Authority (DA)', color='skyblue')
    plt.bar(x + width/2, df['PA'], width, label='Page Authority (PA)', color='salmon')

    # Labels and title
    plt.xlabel('Brand')
    plt.ylabel('Score')
    plt.title("Haldiram Website SEO Performance Indicator (DA & PA)")
    plt.xticks(x, brands, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()