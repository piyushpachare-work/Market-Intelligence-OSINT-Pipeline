import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_seo_da_plot():
    # Load the data
    file_path = "data/Competitor SEO Performance Indi.csv"
    df = pd.read_csv(file_path)

    # Drop rows where Brand or Domain Authority (DA) is missing
    df = df.dropna(subset=['Brand', 'Domain Authority (DA)'])

    # (Optional) Convert Brand to string, just in case
    df['Brand'] = df['Brand'].astype(str)

    # Sort data by Domain Authority
    df_sorted = df.sort_values('Domain Authority (DA)', ascending=True)

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_sorted['Brand'], df_sorted['Domain Authority (DA)'], color='slateblue')

    # Add labels on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                 f"{width:.0f}", va='center', fontsize=9)

    plt.xlabel("Domain Authority (DA)", fontsize=12)
    plt.title("Competitor SEO Performance (Domain Authority)", fontsize=14)
    plt.xlim(0, max(df_sorted['Domain Authority (DA)']) + 10)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf