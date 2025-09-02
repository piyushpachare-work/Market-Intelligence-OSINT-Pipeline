import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_platform_ratings_bar():
    # Step 1: Read the CSV file
    df = pd.read_csv("sectionCdata/online_rating.csv")

    # Step 2: Plotting the bar chart
    plt.figure(figsize=(8, 5))
    bars = plt.bar(df['Platform'], df['Assumed Average Rating (out of 5)'], color=['orange', 'green', 'blue', 'red'])

    # Step 3: Add value labels on top of each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, f"{yval:.1f}", ha='center', fontsize=12)

    # Step 4: Styling the chart
    plt.ylim(0, 5)
    plt.ylabel("Average Rating (out of 5)", fontsize=12)
    plt.title("Haldiram Average Online Rating per Platform", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()