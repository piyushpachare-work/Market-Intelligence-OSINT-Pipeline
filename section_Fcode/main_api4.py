from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = FastAPI()
CSV_PATH = "section_FCSV/KPI4.csv"

@app.get("/F/kpi4/chart")
def kpi4_country_chart():
    if not os.path.exists(CSV_PATH):
        return JSONResponse(status_code=404, content={"error": f"{CSV_PATH} not found."})

    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8-sig')
        if 'Country' not in df.columns:
            return JSONResponse(status_code=400, content={"error": "'Country' column not found in CSV."})

        df['Country'] = df['Country'].astype(str).str.strip()
        country_counts = df['Country'].value_counts()

        if country_counts.empty:
            return JSONResponse(content={"info": "No country data to display."})

        # Create bar chart
        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Paired(np.linspace(0, 1, len(country_counts)))
        bars = ax.bar(country_counts.index, country_counts.values, color=colors, edgecolor='black')

        ax.set_title("Mentions by Country")
        ax.set_xlabel("Country")
        ax.set_ylabel("Number of Mentions")
        plt.xticks(rotation=45, ha='right')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, height + 0.1, int(height), ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
