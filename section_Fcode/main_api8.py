from fastapi import FastAPI, Response
import pandas as pd
import re
import io
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

app = FastAPI()

def generate_sentiment_chart(csv_filepath='section_FCSV/KPI8.csv'):
    try:
        df = pd.read_csv(csv_filepath, encoding='utf-8-sig')
    except Exception:
        return None

    df.columns = df.columns.map(lambda x: x.strip() if isinstance(x, str) else x)
    if df.columns[0].startswith('\ufeff'):
        df.rename(columns={df.columns[0]: df.columns[0].replace('\ufeff', '').strip()}, inplace=True)

    expected_cols = ['Comment Snippet (Illustrative)', 'Sentiment/Severity Assessment']
    if not all(col in df.columns for col in expected_cols):
        return None

    df_processed = df[expected_cols].copy()
    df_processed['Sentiment/Severity Assessment'] = df_processed['Sentiment/Severity Assessment'].astype(str).str.strip().fillna('N/A')
    df_processed['Comment Snippet (Illustrative)'] = df_processed['Comment Snippet (Illustrative)'].astype(str).str.strip().fillna('No comment provided')

    greenwashing_keywords = [
        'greenwashing', 'greenwash', 'skeptical', 'cynical', 'doubt', 'misleading',
        'not enough', 'vague statement', 'actions > words', 'demanding proof',
        'questioning claim', 'no real data', 'empty promise', 'lip service',
        'feels like talk', 'not convinced', 'unsubstantiated', 'deceptive',
        'marketing gimmick', 'show the data', 'critical omission'
    ]
    pattern = re.compile(r'\b(' + '|'.join(greenwashing_keywords) + r')\b', re.IGNORECASE)

    filter_condition = (
        df_processed['Comment Snippet (Illustrative)'].apply(lambda x: bool(pattern.search(x))) |
        df_processed['Sentiment/Severity Assessment'].apply(lambda x: bool(pattern.search(x))) |
        df_processed['Sentiment/Severity Assessment'].str.contains('critical', case=False, na=False) |
        df_processed['Sentiment/Severity Assessment'].str.contains('negative', case=False, na=False)
    )
    df_greenwashing_related = df_processed[filter_condition]

    if df_greenwashing_related.empty:
        return None

    sentiment_counts = Counter(df_greenwashing_related['Sentiment/Severity Assessment'])
    if not sentiment_counts:
        return None

    top_n = 10
    common_sentiments = sentiment_counts.most_common(top_n)
    sentiment_labels = [item[0][:30] + ('...' if len(item[0]) > 30 else '') for item in common_sentiments]
    sentiment_values = [item[1] for item in common_sentiments]

    sentiment_labels.reverse()
    sentiment_values.reverse()

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, max(5, len(sentiment_labels) * 0.5)))
    bars = ax.barh(sentiment_labels, sentiment_values, color=plt.cm.Spectral(np.linspace(0.2, 0.8, len(sentiment_labels))))
    ax.set_xlabel("Number of Mentions", fontsize=10)
    ax.set_title(f"Top {len(sentiment_labels)} Sentiment/Severity Assessments\n(among Skeptical/Critical Comments)", fontsize=12)
    plt.yticks(fontsize=9)
    plt.xticks(fontsize=9)
    for bar in bars:
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                f'{bar.get_width()}', va='center', ha='left', fontsize=8)

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=90)
    buf.seek(0)
    plt.close(fig)

    return buf

@app.get("/F/kpi8/chart", response_class=Response)
async def kpi8_chart():
    img_buffer = generate_sentiment_chart()
    if img_buffer is None:
        return Response(content="No chart available or error in processing.", media_type="text/plain", status_code=404)

    return Response(content=img_buffer.read(), media_type="image/png")
