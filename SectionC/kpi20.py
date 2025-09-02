import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_news_mention_frequency_plot():
    # Load the CSV file
    df = pd.read_csv('sectionCdata/unique_news_mentions.csv')

    # Sort by Unique News Mentions descending for better visualization
    df_sorted = df.sort_values(by='Unique News Mentions', ascending=False)

    # Plotting
    plt.figure(figsize=(10,6))
    bars = plt.bar(df_sorted['Brand'], df_sorted['Unique News Mentions'], color='skyblue')

    # Adding value labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=11)

    plt.title("Haldiram News Mention Frequency vs Competitors", fontsize=16)
    plt.xlabel("Brand", fontsize=13)
    plt.ylabel("Unique News Mentions", fontsize=13)
    plt.ylim(0, max(df_sorted['Unique News Mentions']) + 2)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()