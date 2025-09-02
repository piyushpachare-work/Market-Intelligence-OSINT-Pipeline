import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_news_sentiment_pie():
    data = pd.read_csv("sectionCdata/news_sentiment.csv", encoding="cp1252")
    sentiment_counts = data['Overall Sentiment'].value_counts()

    plt.figure(figsize=(6, 6))
    plt.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        startangle=90
    )
    plt.title("Sentiment Distribution (Positive, Negative, Neutral)")
    plt.axis('equal')  # Ensures circle shape
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()