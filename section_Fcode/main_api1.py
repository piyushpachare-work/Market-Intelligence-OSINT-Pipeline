from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import io
import os

app = FastAPI()

CSV_PATH = "section_FCSV/KPI1.csv"

def load_and_prepare_data():
    try:
        df = pd.read_csv(CSV_PATH, usecols=range(12), nrows=25, encoding='utf-8')
    except Exception as e:
        raise Exception(f"Failed to read {CSV_PATH}: {e}")

    df.columns = df.columns.str.replace('\ufeff', '', regex=False)
    if df.columns[0] != "Month_Name":
        df.rename(columns={df.columns[0]: "Month_Name"}, inplace=True)

    brand_columns = df.columns[2:]
    for col in brand_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=brand_columns, how='all', inplace=True)
    df["Continuous_Month"] = range(1, len(df) + 1)
    return df, brand_columns.tolist()

@app.get("/F/KPI1")
def get_trend_chart():
    if not os.path.exists(CSV_PATH):
        return JSONResponse(status_code=404, content={"error": "KPI1.csv not found."})
    
    try:
        df, brands = load_and_prepare_data()
        x_period = np.arange(1, 13)

        valid_brands = []
        for brand in brands:
            p12 = df[brand].iloc[0:12].values
            l12 = df[brand].iloc[12:24].values
            if len(p12) < 12 or len(l12) < 12 or np.isnan(p12).any() or np.isnan(l12).any():
                continue
            valid_brands.append(brand)

        if not valid_brands:
            return JSONResponse(content={"error": "No valid brand data to plot."})

        fig_height = len(valid_brands) * 4
        plt.figure(figsize=(15, fig_height))

        for idx, brand in enumerate(valid_brands):
            p12 = df[brand].iloc[0:12].values
            l12 = df[brand].iloc[12:24].values
            slope_p, intercept_p, *_ = linregress(x_period, p12)
            slope_l, intercept_l, *_ = linregress(x_period, l12)

            plt.subplot(len(valid_brands), 1, idx + 1)
            plt.plot(df["Continuous_Month"], df[brand], marker='o', label=f"{brand} Actual Data")
            plt.plot(df["Continuous_Month"].iloc[0:12], x_period * slope_p + intercept_p, 'orange', linestyle='--', label=f"P12M Slope: {slope_p:.2f}")
            plt.plot(df["Continuous_Month"].iloc[12:24], x_period * slope_l + intercept_l, 'green', linestyle='--', label=f"L12M Slope: {slope_l:.2f}")
            plt.title(f"{brand}")
            plt.xlabel("Month")
            plt.ylabel("Trend Score")
            plt.legend()
            plt.grid(True)

        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return Response(content=buf.read(), media_type="image/png")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
