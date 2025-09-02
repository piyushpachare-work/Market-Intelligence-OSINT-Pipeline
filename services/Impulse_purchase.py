# services/impulse_kpi_chart.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_impulse_kpi_chart():
    try:
        csv_path = Path("KPI_Data") / "impulse_purchase_Mentions.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        required_columns = ["Platform", "Impulse Indicator Strength"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")

        grouped = df.groupby(["Platform", "Impulse Indicator Strength"]).size().reset_index(name="Count")

        platforms = grouped["Platform"].unique()
        strengths = grouped["Impulse Indicator Strength"].unique()

        fig, ax = plt.subplots(figsize=(16, 7))
        bar_width = 0.2
        x_pos = list(range(len(platforms)))

        for i, strength in enumerate(strengths):
            counts = [
                grouped[(grouped["Platform"] == platform) & (grouped["Impulse Indicator Strength"] == strength)]["Count"].sum()
                for platform in platforms
            ]
            positions = [x + bar_width * i for x in x_pos]
            ax.bar(positions, counts, bar_width, label=str(strength))

        ax.set_xlabel("Platform")
        ax.set_ylabel("Impulse Purchase Count")
        ax.set_title("Impulse Purchase Counts by Platform and Indicator Strength")
        ax.set_xticks([x + bar_width for x in x_pos])
        ax.set_xticklabels(platforms, rotation=45, ha='right')
        ax.legend()

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
