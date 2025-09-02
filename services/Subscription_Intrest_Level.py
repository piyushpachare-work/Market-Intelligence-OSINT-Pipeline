# services/subscription_interest_level.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import io
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_subscription_pie_chart():
    try:
        csv_path = Path("KPI_Data") / "Subscription_Intrest.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        if 'Subscription Interest Level' not in df.columns:
            raise ValueError("Column 'Subscription Interest Level' not found in the CSV.")

        data = df['Subscription Interest Level'].value_counts()

        fig, ax = plt.subplots()
        ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
