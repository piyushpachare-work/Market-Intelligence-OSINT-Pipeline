# services/platform_funnel_kpi.py

import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse
from fastapi import HTTPException
from pathlib import Path

def get_platform_funnel_kpi_chart():
    try:
        # Use pathlib for cross-platform compatibility
        csv_path = Path("KPI_Data") / "platform_role.csv"
        chart_dir = Path("static") / "charts"
        chart_path = chart_dir / "platform_funnel_kpi_chart.png"

        # Check if CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        # Read data
        df = pd.read_csv(csv_path)

        # Group and transform data
        grouped = df.groupby(['Platform', 'Inferred Funnel Stage']).size().unstack(fill_value=0)
        platforms = grouped.index.tolist()
        funnel_stages = grouped.columns.tolist()
        x = range(len(platforms))
        bar_width = 0.1

        # Plot chart
        plt.figure(figsize=(12, 6))
        for i, stage in enumerate(funnel_stages):
            plt.bar([pos + i * bar_width for pos in x], grouped[stage], width=bar_width, label=stage)

        plt.xticks([pos + bar_width * (len(funnel_stages)/2) for pos in x], platforms, rotation=45, ha='right')
        plt.ylabel("Count")
        plt.title("Distribution of Inferred Funnel Stages by Platform")
        plt.legend(title='Funnel Stage')
        plt.tight_layout()

        # Ensure output directory and save chart
        chart_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(chart_path, dpi=200)
        plt.close()

        return FileResponse(chart_path, media_type='image/png')

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
