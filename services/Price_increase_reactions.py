import pandas as pd
import matplotlib.pyplot as plt
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path

app = FastAPI()

def load_reactions(csv_path):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")
    
    df = pd.read_csv(csv_file)
    # Strip leading/trailing spaces from columns
    df.columns = df.columns.str.strip()
    sentiment_counts = df['Sentiment'].value_counts()
    positive_count = sentiment_counts.get('Positive', 0)
    negative_count = sentiment_counts.get('Negative', 0)
    labels = ['Positive', 'Negative']
    sizes = [positive_count, negative_count]
    return labels, sizes

def create_pie_chart(labels, sizes):
    plt.figure(figsize=(6,6))
    colors = ['#66b3ff', '#ff6666']  # blue for positive, red for negative
    explode = (0.1, 0)  # explode first slice (Positive) slightly

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
            colors=colors, explode=explode, shadow=True)

    plt.title("Response to Price Increase Justification - Sentiment Distribution")
    plt.axis('equal')  # Equal aspect ratio for pie chart

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf