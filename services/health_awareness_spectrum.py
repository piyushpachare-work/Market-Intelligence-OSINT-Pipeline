# services/health_awareness_chart.py

import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from pathlib import Path
import io

def get_health_awareness_chart():
    try:
        csv_path = Path("KPI_Data") / "health_spectrum.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        if 'Health Awareness Level' not in df.columns or 'Mentions (Count)' not in df.columns:
            raise ValueError("Required columns missing in the CSV.")

        grouped = df.groupby("Health Awareness Level")["Mentions (Count)"].sum()

        # Define colors
        colors = {
            "Low": "#FF6961",
            "Moderate": "#FFD700",
            "High": "#77DD77"
        }

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            grouped,
            labels=grouped.index,
            autopct='%1.1f%%',
            colors=[colors.get(level, "#D3D3D3") for level in grouped.index],
            startangle=90
        )
        ax.set_title("Health Awareness Spectrum")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
