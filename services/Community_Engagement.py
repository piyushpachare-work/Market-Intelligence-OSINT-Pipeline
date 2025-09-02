# services/kpi_community_engagement.py

from fastapi import Response, HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def community_engagement_chart():
    try:
        # Paths
        csv_path = Path("KPI_data") / "community_engagement.csv"
        chart_dir = Path("static") / "charts"
        chart_path = chart_dir / "community_engagement.png"

        # Check if CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        # Read and process data
        df = pd.read_csv(csv_path)
        df.fillna("None", inplace=True)
        grouped = df.groupby("Platform").size().sort_values(ascending=False)

        # Plot chart
        plt.figure(figsize=(10, 6))
        grouped.plot(kind="bar", color="orange")
        plt.title("Community Engagement by Platform")
        plt.xlabel("Platform")
        plt.ylabel("Number of Groups")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Save chart
        chart_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(chart_path)
        plt.close()

        return Response(content=chart_path.read_bytes(), media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
