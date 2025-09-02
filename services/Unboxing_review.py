import csv
from collections import Counter
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

CSV_PATH = Path("KPI_data") / "Unboxing_Experience.csv"

def load_review_sentiments():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")

    sentiment_counts = Counter()
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if "User Sentiment" not in reader.fieldnames:
                raise ValueError(f"'User Sentiment' column not found. Found: {reader.fieldnames}")
            for row in reader:
                sentiment = row["User Sentiment"].strip().lower()
                if sentiment in ("positive", "negative"):
                    sentiment_counts[sentiment] += 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")

    return sentiment_counts

def get_unboxing_sentiment_chart():
    try:
        sentiment_counts = load_review_sentiments()
        labels = ['Positive', 'Negative']
        values = [sentiment_counts.get('positive', 0), sentiment_counts.get('negative', 0)]

        plt.figure(figsize=(6, 4))
        bars = plt.bar(labels, values, color=['#A8DADC', '#F4A261'])
        plt.title('Number of Positive and Negative Reviews')
        plt.ylabel('Count')
        plt.xlabel('Sentiment')

        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
