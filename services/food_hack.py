# services/hacktype_chart.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_hacktype_bar_chart(csv_path=Path("KPI_data") / "food_hack_mentions.csv"):
    try:
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        col = 'Hack Type'
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in CSV. Columns found: {df.columns.tolist()}")

        counts = df[col].value_counts()

        plt.figure(figsize=(8,5))
        counts.plot(kind='bar', color='skyblue')
        plt.xlabel('Hack Type')
        plt.ylabel('Count')
        plt.title('Hack Type Counts')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return StreamingResponse(buf, media_type='image/png')

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
