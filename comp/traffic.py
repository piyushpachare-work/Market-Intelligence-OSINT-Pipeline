import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_traffic_plot():
    # Load the CSV
    file_path = "data/Competitor Website Traffic Esti.csv"
    df = pd.read_csv(file_path)

    # Clean and convert visit numbers
    df['Monthly Visits'] = pd.to_numeric(df['Monthly Visits'].str.replace('K', 'e3').str.replace('M', 'e6'), errors='coerce')

    # Drop rows with no visit data
    df = df.dropna(subset=['Monthly Visits'])

    # Sort by Monthly Visits
    df_sorted = df.sort_values('Monthly Visits', ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_sorted['Brand'], df_sorted['Monthly Visits'], color='teal')

    # Add labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 1000, bar.get_y() + bar.get_height() / 2,
                 f"{int(width):,}", va='center', fontsize=9)

    plt.xlabel("Monthly Visits", fontsize=12)
    plt.title("Competitor Website Traffic Estimates", fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf