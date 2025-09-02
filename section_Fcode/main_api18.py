from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

app = FastAPI(title="KPI 18: Health Claim Scrutiny Index")

CSV_FILENAME = "section_FCSV/KPI18.csv"

@app.get("/F/kpi18/visualize", summary="Visualize KPI 18 as image")
def get_kpi18_visualization():
    if not os.path.exists(CSV_FILENAME):
        raise HTTPException(status_code=404, detail=f"CSV file '{CSV_FILENAME}' not found.")

    try:
        df = pd.read_csv(CSV_FILENAME)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")

    required_columns = ['Brand Mentioned', 'Health Claim', 'Sentiment', 'Severity Level']
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing)}")

    df_brand = df[df['Brand Mentioned'].str.strip().str.lower() == 'haldiram'].copy()
    if df_brand.empty:
        raise HTTPException(status_code=404, detail="No data found for 'Haldiram'.")

    irrelevant_topics = [
        'Brand Recognition', 'Trademark Status', 'Market Expansion', 'Market Growth',
        'Revenue Growth', 'Market Share Growth', 'Facility Expansion',
        'International Expansion', 'Data Security', 'Environmental Impact',
        'New Product Launch', 'Product Development', 'Product Reform',
        'Sustainability', 'Performance', 'Recognition', 'Brand Expansion'
    ]

    irrelevant_set = set([x.lower() for x in irrelevant_topics])
    df_brand['Health Claim'] = df_brand['Health Claim'].astype(str).fillna('')
    df_relevant = df_brand[~df_brand['Health Claim'].str.strip().str.lower().isin(irrelevant_set)].copy()

    df_relevant['Sentiment'] = df_relevant['Sentiment'].astype(str).str.strip().str.lower()
    df_relevant['Severity Level'] = df_relevant['Severity Level'].astype(str).str.strip().str.lower()

    scrutiny_filter = (
        (df_relevant['Sentiment'] == 'negative') |
        (df_relevant['Severity Level'].isin(['medium', 'high']))
    )
    df_scrutiny = df_relevant[scrutiny_filter]

    if df_scrutiny.empty:
        raise HTTPException(status_code=204, detail="No scrutiny incidents found.")

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart - Severity Level
    severity_counts = df_scrutiny['Severity Level'].value_counts()
    axs[0].bar(severity_counts.index, severity_counts.values, color='salmon', edgecolor='black')
    axs[0].set_title("Scrutiny by Severity Level")
    axs[0].set_xlabel("Severity Level")
    axs[0].set_ylabel("Number of Incidents")
    axs[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Pie chart - Sentiment
    sentiment_counts = df_scrutiny['Sentiment'].value_counts()
    axs[1].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
               colors=['lightcoral', 'gold', 'lightgreen'], startangle=140)
    axs[1].set_title("Sentiment Distribution")

    plt.tight_layout()

    # Save plot to memory buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
