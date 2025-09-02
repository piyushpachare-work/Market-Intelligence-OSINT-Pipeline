import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_share_of_search_pie():
    # Step 1: Load the data
    df = pd.read_csv("sectionCdata/share_of_search.csv")

    # Step 2: Filter required columns
    df = df[['Brand', 'Share of Search %']]

    # Step 3: Plot pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(df['Share of Search %'], labels=df['Brand'], autopct='%1.1f%%', startangle=140)
    plt.title("Haldiram vs Competitors – Share of Search (%)", fontsize=14)
    plt.axis('equal')  # Equal aspect ratio ensures pie is a circle.
    plt.tight_layout()

    # Step 4: Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()