# services/purchase_frequency_chart.py

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import HTTPException

def generate_purchase_frequency_chart():
    try:
        # Safe paths
        csv_path = Path("KPI_Data") / "purchase_frequency.csv"
        chart_dir = Path("static") / "charts"
        chart_path = chart_dir / "purchase_frequency_mentions.png"

        # Check CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        # Read data
        df = pd.read_csv(csv_path)

        # Process data
        freq_counts = df['Interpreted Frequency'].value_counts().sort_values(ascending=False)

        # Plot
        plt.figure(figsize=(12, 6))
        bars = plt.bar(freq_counts.index, freq_counts.values, color='skyblue')
        plt.title("Purchase Frequency Mentions Count")
        plt.ylabel("Number of Mentions")
        plt.xlabel("Interpreted Frequency")
        plt.xticks(rotation=45, ha='right')

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(int(height)), ha='center', va='bottom')

        plt.tight_layout()

        # Save chart
        chart_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(chart_path, dpi=200)
        plt.close()

        return FileResponse(chart_path, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
