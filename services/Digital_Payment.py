# services/payment_issues_chart.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_payment_issues_chart(csv_path=Path("KPI_data") / "Digital_Payment_feedback.csv"):
    try:
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        required_cols = ['Payment Method', 'Transaction Outcome']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing columns in CSV. Found columns: {df.columns.tolist()}")

        summary = df.groupby(['Payment Method', 'Transaction Outcome']).size().unstack(fill_value=0)

        plt.figure(figsize=(10,6))
        colors = ['#AEC6CF', '#FFB347']  # pastel blue & orange
        summary.plot(kind='bar', stacked=True, color=colors)

        plt.title('Payment Method - Success vs Failure Counts')
        plt.xlabel('Payment Method')
        plt.ylabel('Number of Transactions')
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Transaction Outcome')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
