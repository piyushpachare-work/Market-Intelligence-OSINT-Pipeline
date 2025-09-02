# services/homemade_vs_local_chart.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def create_chart_image():
    try:
        csv_path = Path("KPI_Data") / "homemade_vs_local_comparison.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        required_columns = ["Product Category", "Comparison Type", "Sentiment"]
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"Required columns missing. Found columns: {df.columns.tolist()}")

        df = df[required_columns]
        grouped = df.groupby(required_columns).size().reset_index(name="Count")

        fig, ax = plt.subplots(figsize=(18, 6))
        categories = grouped["Product Category"].unique()
        comparison_types = grouped["Comparison Type"].unique()
        sentiments = grouped["Sentiment"].unique()

        bar_width = 0.2
        x_pos = list(range(len(comparison_types)))

        for i, sentiment in enumerate(sentiments):
            for j, category in enumerate(categories):
                subset = grouped[(grouped["Sentiment"] == sentiment) & (grouped["Product Category"] == category)]
                counts = [subset[subset["Comparison Type"] == ct]["Count"].sum() for ct in comparison_types]
                positions = [x + bar_width * i + bar_width * j * len(sentiments) for x in x_pos]
                ax.bar(positions, counts, bar_width, label=f"{sentiment} - {category}")

        ax.set_xlabel("Comparison Type")
        ax.set_ylabel("Count")
        ax.set_title("Sentiment by Product Category and Comparison Type")
        ax.set_xticks([x + bar_width for x in x_pos])
        ax.set_xticklabels(comparison_types, rotation=45)
        ax.legend()

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
