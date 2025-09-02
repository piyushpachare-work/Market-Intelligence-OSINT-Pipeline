# services/issue_type_chart.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_issue_type_chart():
    try:
        csv_path = Path("KPI_Data") / "return_refund_issues.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        if 'Issue Type' not in df.columns:
            raise ValueError(f"'Issue Type' column not found. Available columns: {df.columns.tolist()}")

        issue_counts = df['Issue Type'].value_counts()

        plt.figure(figsize=(8, 5))
        issue_counts.plot(kind='bar', color='skyblue')
        plt.title('Issue Type Counts')
        plt.ylabel('Count')
        plt.xlabel('Issue Type')
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
