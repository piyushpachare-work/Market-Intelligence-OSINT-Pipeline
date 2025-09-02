import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_mention_volume_plot():
    # Step 1: Load the data
    df = pd.read_csv("sectionCdata/mention_volume.csv")

    # Step 2: Convert 'Dates' to datetime
    df['Dates'] = pd.to_datetime(df['Dates'])

    # Step 3: Plot line chart
    plt.figure(figsize=(10, 5))
    plt.plot(df['Dates'], df['Twitter mentions'], marker='o', color='blue')
    plt.title("Haldiram Social Media Mention Volume (Twitter)", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Mentions")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Step 4: Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()