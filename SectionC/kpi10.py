import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_engagement_rate_plot():
    # Load and prepare data
    df = pd.read_csv("sectionCdata/engagement_rate.csv")
    df.columns = df.columns.str.strip()
    df["Engagement Rate (%)"] = pd.to_numeric(df["Engagement Rate (%)"], errors='coerce')
    df_sorted = df.sort_values(by="Engagement Rate (%)", ascending=True)

    # Create color list
    colors = plt.cm.tab20.colors  # A diverse colormap with different distinct colors
    brand_colors = [colors[i % len(colors)] for i in range(len(df_sorted))]

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.barh(
        df_sorted["Engagement Rate (Estimated)"],
        df_sorted["Engagement Rate (%)"],
        color=brand_colors
    )

    # Add values to the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                 f'{width:.2f}%', va='center')

    # Labels and layout
    plt.xlabel("Engagement Rate (%)")
    plt.title("Social Media Engagement Rate by Brand")
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()