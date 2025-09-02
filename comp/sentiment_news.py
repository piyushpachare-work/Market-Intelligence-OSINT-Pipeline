import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_sentiment_pie_chart(brand=None):
    file_path = "data/news n mentions + sentiment.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    if not {'Brand', 'Sentiment'}.issubset(df.columns):
        raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")
    sentiment_colors = {
        'Positive': '#4CAF50',
        'Neutral': '#FF9800',
        'Negative': '#F44336'
    }
    if brand is None:
        # If no brand specified, aggregate all
        sentiment_counts = df['Sentiment'].value_counts()
        title = "Sentiment Breakdown - All Brands"
    else:
        brand_df = df[df['Brand'] == brand]
        sentiment_counts = brand_df['Sentiment'].value_counts()
        title = f"Sentiment Breakdown - {brand}"
    plt.figure(figsize=(6, 5))
    sentiment_counts.plot(
        kind='pie',
        colors=[sentiment_colors.get(s, '#999999') for s in sentiment_counts.index],
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title(title)
    plt.ylabel('')
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf