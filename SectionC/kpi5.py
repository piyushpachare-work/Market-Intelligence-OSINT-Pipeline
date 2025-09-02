import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_kpi5_plot():
    # Step 1: Load the data
    df = pd.read_csv("sectionCdata/sentiment_score.csv")

    # Step 2: Convert percentages to actual values (optional for better pie display)
    df['Percentage'] = df['Percentage'] * 100

    # Step 3: Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(
        df['Percentage'],
        labels=df['Sentiment'],
        autopct='%1.1f%%',
        startangle=140,
        colors=['#90EE90', '#FF9999', '#D3D3D3']
    )
    plt.title("Haldiram Social Media Sentiment Breakdown", fontsize=14)
    plt.tight_layout()

    # Step 4: Save plot to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()