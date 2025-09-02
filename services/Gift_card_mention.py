# services/gift_card_user_type_chart.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

CSV_PATH = Path("KPI_Data") / "Gift_card_mentions.csv"

def create_user_type_pie_chart():
    try:
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"CSV file not found at: {CSV_PATH}")

        df = pd.read_csv(CSV_PATH)

        col = 'User Type (First-time/Repeat)'
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV. Columns found: {df.columns.tolist()}")

        counts = df[col].value_counts()
        repeat_count = counts.get('Repeat', 0)
        first_time_count = counts.get('First-time', 0)

        labels = ['Repeat', 'First-time']
        sizes = [repeat_count, first_time_count]
        colors = ['skyblue', 'salmon']

        plt.figure(figsize=(6,6))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=120)
        plt.title('User Type Distribution (Repeat vs First-time)')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
