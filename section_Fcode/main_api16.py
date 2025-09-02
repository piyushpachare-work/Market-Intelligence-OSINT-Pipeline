from fastapi import FastAPI, Response
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import io
import base64
import os

app = FastAPI()

@app.get("/F/kpi16/visualize", response_class=Response, responses={200: {"content": {"image/png": {}}}})
def visualize_kpi16():
    file_path = "section_FCSV/KPI16.csv"

    if not os.path.isfile(file_path):
        return Response(content="CSV file not found.", media_type="text/plain", status_code=404)

    # Step 1: Load CSV
    df = pd.read_csv(file_path, encoding='windows-1252')

    # Step 2: Combine text columns
    text_columns = df.select_dtypes(include='object').columns
    df['combined_text'] = df[text_columns].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    # Step 3: Define keywords
    keywords = [
        'ethical sourcing', 'sustainably sourced', 'fair trade', 'responsibly sourced',
        'certified ethical', 'palm oil', 'cocoa', 'cashews', 'organic', 'traceability'
    ]

    # Step 4: Keyword mention detection
    def has_mention(text):
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)

    df['mention'] = df['combined_text'].apply(has_mention)
    mentions_df = df[df['mention'] == True].copy()

    if mentions_df.empty:
        return Response(content="No ethical sourcing mentions found.", media_type="text/plain")

    # Step 5: Sentiment analysis
    mentions_df['sentiment_score'] = mentions_df['combined_text'].apply(lambda text: TextBlob(text).sentiment.polarity)

    def categorize_sentiment(score):
        if score > 0.1:
            return 'Positive'
        elif score < -0.1:
            return 'Negative'
        else:
            return 'Neutral'

    mentions_df['sentiment'] = mentions_df['sentiment_score'].apply(categorize_sentiment)

    sentiment_summary = mentions_df['sentiment'].value_counts()

    # Step 6: Plot
    plt.figure(figsize=(6, 4))
    sentiment_summary.plot(kind='bar', color='skyblue')
    plt.title("Sentiment Distribution on Ethical Sourcing Mentions")
    plt.xlabel("Sentiment")
    plt.ylabel("Frequency")
    plt.tight_layout()

    # Step 7: Convert plot to PNG response
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")
