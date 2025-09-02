import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_traffic_sources_pie():
    # Read the CSV file
    df = pd.read_csv("sectionCdata/traffi_sources.csv")

    # Convert percentage strings to float values
    df["Percentage"] = df["Percentage"].str.replace('%', '').astype(float)

    # Plotting the pie chart
    plt.figure(figsize=(8, 6))
    colors = plt.get_cmap('Set3').colors  # Optional: colorful palette
    plt.pie(df["Percentage"], labels=df["Traffic Source"], autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title("Haldiram Website Top Traffic Sources")
    plt.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()