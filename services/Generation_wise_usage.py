# services/cross_generation_usage.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_cross_generation_chart():
    try:
        csv_path = Path("KPI_Data") / "generation_wise_consumption.csv"

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()

        if 'Generation' not in df.columns:
            raise ValueError("Column 'Generation' not found in the CSV.")

        gen_counts = df['Generation'].value_counts()

        # Plot
        plt.figure(figsize=(8, 5))
        gen_counts.plot(kind='bar', color='skyblue')
        plt.xlabel("Generation")
        plt.ylabel("Number of Mentions")
        plt.title("Cross-Generation Usage")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save to memory
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        return StreamingResponse(img, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
