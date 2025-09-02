import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_engagement_plot():
    # Load the file
    file_path = "data/Competitor Social Media Engagem.csv"
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()
    df['Company'] = df['Company'].astype(str).str.strip()

    # Convert engagement values
    df['Avg(Likes + comments)'] = pd.to_numeric(df['Avg(Likes + comments)'], errors='coerce')

    # Drop any rows with missing 'Company' or engagement data
    df = df.dropna(subset=['Company', 'Avg(Likes + comments)'])

    # Sort for better visuals
    df_sorted = df.sort_values(by='Avg(Likes + comments)', ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_sorted['Company'], df_sorted['Avg(Likes + comments)'], color='orchid')

    # Annotate bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 5, bar.get_y() + bar.get_height() / 2,
                 f"{width:.1f}", va='center', fontsize=9)

    plt.xlabel("Avg Engagement (Likes + Comments)", fontsize=12)
    plt.title("Estimated Social Media Engagement per Post", fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf