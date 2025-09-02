import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_bounce_rate_plot():
    # Load the data
    file_path = "data/bounce rate.csv"
    df = pd.read_csv(file_path)

    # Clean bounce rate column: remove '%' if present and convert to float
    df['Bounce Rate (%)'] = df['Bounce Rate (%)'].astype(str).str.replace('%', '').astype(float)

    # Sort by bounce rate
    df_sorted = df.sort_values('Bounce Rate (%)', ascending=False)

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_sorted['Company'], df_sorted['Bounce Rate (%)'], color='salmon')

    # Add labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                 f"{width:.2f}%", va='center', fontsize=9)

    plt.xlabel("Bounce Rate (%)", fontsize=12)
    plt.title("Estimated Website Bounce Rates (MozBar)", fontsize=14)
    plt.xlim(0, 100)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf