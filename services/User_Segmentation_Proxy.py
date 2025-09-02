# services/user_segmentation_proxy.py

import pandas as pd
import matplotlib.pyplot as plt
from fastapi import Response, HTTPException
from pathlib import Path

def user_segmentation_proxy() -> Response:
    try:
        # 1️⃣ Define paths safely
        data_path = Path("KPI_Data") / "user_segmentation_proxy.csv"
        chart_dir = Path("static") / "charts"
        chart_path = chart_dir / "user_segmentation.png"

        # 2️⃣ Load CSV (fail with clear error if missing)
        if not data_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {data_path}")

        df = pd.read_csv(data_path)
        df.fillna("N/A", inplace=True)
        df["Cluster_Label"] = df["Inferred User Cluster"] + " (" + df["Language Style"] + ")"

        # 3️⃣ Count occurrences
        counts = df["Cluster_Label"].value_counts().sort_values()

        # 4️⃣ Plot chart
        plt.figure(figsize=(10, max(6, len(counts) * 0.4)))
        counts.plot(kind="barh")
        plt.title("User Segmentation by Cluster & Language")
        plt.xlabel("Count")
        plt.ylabel("User Cluster (Language)")
        plt.tight_layout()

        # 5️⃣ Save chart
        chart_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(chart_path)
        plt.close()

        # 6️⃣ Serve chart as PNG
        with open(chart_path, "rb") as img:
            return Response(content=img.read(), media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
