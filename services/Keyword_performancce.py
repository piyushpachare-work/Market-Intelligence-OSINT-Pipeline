import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path

app = FastAPI()

def generate_high_intent_keyword_trend_chart(csv_path):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found: {csv_file}")

    df = pd.read_csv(csv_file)
    keyword_totals = df.groupby('Keyword')['Search Volume'].sum().sort_values(ascending=False)

    plt.figure(figsize=(10,6))
    keyword_totals.plot(kind='bar', color='skyblue')
    plt.title('Total Search Volume by High-Intent Keywords')
    plt.xlabel('Keyword')
    plt.ylabel('Total Search Volume')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf