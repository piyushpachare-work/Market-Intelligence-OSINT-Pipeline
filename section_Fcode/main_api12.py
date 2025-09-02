from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os

app = FastAPI(title="KPI 12: DTC Adoption Visualization")

# Use relative path exactly as requested
CSV_FILENAME = "section_FCSV/KPI12.csv"

if not os.path.exists(CSV_FILENAME):
    raise FileNotFoundError(f"CSV file not found at: {CSV_FILENAME}")

def load_and_process_data():
    df = pd.read_csv(CSV_FILENAME, encoding='ISO-8859-1')
    df['Monthly Search Volume (India)'] = df['Monthly Search Volume (India)'].str.replace(',', '').astype(int)
    df['DTC Website'] = df['Has DTC Website? (Yes/No)'].str.strip().str.lower() == 'yes'

    grouped = df.groupby('Category').agg({
        'Competitor Name': 'count',
        'DTC Website': 'sum',
        'Monthly Search Volume (India)': 'sum'
    }).rename(columns={
        'Competitor Name': 'Total Competitors',
        'DTC Website': 'Competitors with DTC',
        'Monthly Search Volume (India)': 'Total Search Volume'
    })

    grouped['DTC Adoption Rate (%)'] = (grouped['Competitors with DTC'] / grouped['Total Competitors']) * 100

    def assess_viability(row):
        if row['DTC Adoption Rate (%)'] >= 70 and row['Total Search Volume'] >= 20000:
            return 'High'
        elif row['DTC Adoption Rate (%)'] >= 40 and row['Total Search Volume'] >= 10000:
            return 'Medium'
        else:
            return 'Low'

    grouped['DTC Viability Index'] = grouped.apply(assess_viability, axis=1)
    return grouped.reset_index()

category_data = load_and_process_data()

@app.get("/F/kpi12/visualize")
def get_visualization():
    plt.figure(figsize=(10, 6))
    bars = plt.bar(category_data['Category'], category_data['DTC Adoption Rate (%)'], color='skyblue')
    plt.title("DTC Adoption Rate by Category")
    plt.ylabel("DTC Adoption Rate (%)")
    plt.xlabel("Category")
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.1f}%', ha='center', fontsize=8)

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
