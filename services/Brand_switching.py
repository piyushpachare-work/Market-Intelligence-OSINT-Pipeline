# services/logic.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import HTTPException

def generate_switch_trigger_chart():
    try:
        # Define safe paths
        csv_path = Path("KPI_data") / "Brand_switching_triggers.csv"
        chart_dir = Path("static") / "charts"
        chart_path = chart_dir / "brand_switching_triggers.png"

        # Check if CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        # Read data
        df = pd.read_csv(csv_path)

        # Count frequency of switch triggers
        trigger_counts = df['Switch Trigger (Positive/Negative)'].value_counts()

        # Plot
        plt.figure(figsize=(10, 6))
        trigger_counts.plot(kind='bar', color='skyblue')
        plt.title("Brand Switching Triggers (Mentioned)")
        plt.xlabel("Switch Triggers")
        plt.ylabel("Number of Mentions")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Ensure directory and save
        chart_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(chart_path)
        plt.close()

        return FileResponse(chart_path, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
