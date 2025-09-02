from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import os

app = FastAPI()

CSV_PATH = "section_FCSV/KPI3.csv"

@app.get("/F/kpi3/chart")
def get_platform_chart():
    chart_buffer, error = generate_platform_chart(CSV_PATH)
    if error:
        return JSONResponse(status_code=400, content={"error": error})
    if chart_buffer:
        return Response(content=chart_buffer.getvalue(), media_type="image/png")
    return JSONResponse(content={"info": "No chart to display."})


def generate_platform_chart(csv_filepath):
    try:
        df = pd.read_csv(csv_filepath, encoding='utf-8-sig')
    except FileNotFoundError:
        return None, f"File '{csv_filepath}' not found."
    except Exception as e:
        return None, f"Error reading CSV: {e}"

    expected_cols = ['Mention', 'Category Preference', 'Context/Reason', 'Platforms']
    missing = [col for col in expected_cols if col not in df.columns]
    if missing:
        return None, f"Missing columns: {', '.join(missing)}"

    df = df[expected_cols].copy()
    for col in expected_cols:
        df[col] = df[col].astype(str).str.strip()
        df[col].replace('nan', pd.NA, inplace=True)
    df.dropna(subset=['Mention', 'Category Preference', 'Platforms'], inplace=True)

    if df.empty:
        return None, "No valid data found."

    target_preference = "Namkeen over Sweets"
    df_filtered = df[df['Category Preference'] == target_preference]

    if df_filtered.empty:
        return None, f"No mentions indicating '{target_preference}' found."

    platform_counts = df_filtered['Platforms'].value_counts()
    if platform_counts.empty:
        return None, "No platform data to display."

    # Generate chart
    chart_buffer = io.BytesIO()
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Set3(np.linspace(0, 1, len(platform_counts)))
    bars = ax.bar(platform_counts.index, platform_counts.values, color=colors, edgecolor='black')
    ax.set_title(f"'{target_preference}' Mentions by Platform")
    ax.set_xlabel("Platform")
    ax.set_ylabel("Number of Mentions")
    plt.xticks(rotation=45, ha="right")
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, height + 0.1, int(height), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(chart_buffer, format='png')
    chart_buffer.seek(0)
    plt.close()

    return chart_buffer, None
