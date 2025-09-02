import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_follower_growth_rate_plot():
    # Load the CSV file
    df = pd.read_csv("sectionCdata/follower_growth_rate.csv")

    # Remove % sign and convert Growth Rate to float
    df['Growth Rate'] = df['Growth Rate'].str.rstrip('%').astype(float)

    # Plot bar chart
    plt.figure(figsize=(8,5))
    plt.bar(df['Platform'], df['Growth Rate'], color='skyblue')
    plt.ylabel('Growth Rate (%)')
    plt.title('Haldiram Primary Social Platform Follower Growth Rate')
    plt.ylim(0, df['Growth Rate'].max() + 5)

    # Show exact values on bars
    for i, v in enumerate(df['Growth Rate']):
        plt.text(i, v + 0.3, f"{v:.2f}%", ha='center')

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()