# services/search_behavior.py

import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
from fastapi.responses import StreamingResponse
from pathlib import Path
from fastapi import HTTPException

CSV_FILE_PATH = Path("KPI_Data") / "Search_Behavior.csv"

def generate_search_behavior_evolution_chart():
    if not CSV_FILE_PATH.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found at {CSV_FILE_PATH}")
    
    df = pd.read_csv(CSV_FILE_PATH)

    required_cols = ['Search Query/Keyword', 'Search Trend (Today)', 'Search Trend (1-2 Years Ago)', 'Trend Change (%)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise HTTPException(status_code=400, detail=f"Missing columns in CSV: {missing_cols}")

    df_sorted = df.sort_values(by='Trend Change (%)', ascending=False)

    plt.figure(figsize=(15, 10))

    indices = range(len(df_sorted))
    bar_width = 0.4

    bars_today = plt.bar(indices, df_sorted['Search Trend (Today)'], bar_width, label='Search Trend (Today)', color='green')
    bars_past = plt.bar([i + bar_width for i in indices], df_sorted['Search Trend (1-2 Years Ago)'], bar_width, label='Search Trend (1-2 Years Ago)', color='orange')

    for i, change in enumerate(df_sorted['Trend Change (%)']):
        color_today = 'green' if change > 0 else 'red'
        bars_today[i].set_color(color_today)

    plt.xlabel('Search Queries / Keywords')
    plt.ylabel('Search Trend Value')
    plt.title('Search Behavior Evolution: Today vs 1-2 Years Ago')
    plt.xticks([i + bar_width / 2 for i in indices], df_sorted['Search Query/Keyword'], rotation=90)
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type='image/png')
