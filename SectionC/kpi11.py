import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_content_themes_plot():
    # Load data
    df = pd.read_csv("sectionCdata/content_themes.csv")
    df.columns = df.columns.str.strip()  # Clean column names

    # Sort for better visuals
    df_sorted = df.sort_values(by="Number of High-Engagement Posts", ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    colors = plt.cm.Pastel1.colors[:len(df_sorted)]

    bars = plt.bar(df_sorted["Content Theme"], df_sorted["Number of High-Engagement Posts"], color=colors)

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.1, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10)

    # Customize plot
    plt.title("Top Performing Social Media Content Themes – Haldiram", fontsize=14)
    plt.xlabel("Content Theme", fontsize=12)
    plt.ylabel("High-Engagement Posts", fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()