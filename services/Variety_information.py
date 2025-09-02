# services/information_overload.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from fastapi.responses import StreamingResponse
from pathlib import Path
from fastapi import HTTPException

def generate_information_overload_chart():
    csv_path = Path("KPI_data") / "Feedback_for_variety.csv"
    if not csv_path.exists():
        raise HTTPException(status_code=404, detail=f"CSV file not found at: {csv_path}")

    df = pd.read_csv(csv_path)
    if 'Confusion Type' not in df.columns:
        raise HTTPException(status_code=400, detail="Column 'Confusion Type' not found in CSV")

    confusion_counts = df['Confusion Type'].value_counts()

    plt.figure(figsize=(12, 6))
    bars = plt.bar(confusion_counts.index, confusion_counts.values, color='skyblue')
    plt.title("Information Overload / Simplicity Desire - Confusion Types")
    plt.xlabel("Confusion Type")
    plt.ylabel("Number of Comments")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type='image/png')
