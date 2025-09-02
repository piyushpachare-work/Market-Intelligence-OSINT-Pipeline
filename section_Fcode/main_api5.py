from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import os

app = FastAPI()

def find_header_row(csv_filepath, keywords):
    with open(csv_filepath, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            if all(keyword in line for keyword in keywords):
                return i
    return None

def analyze_subsegment_growth_robust(csv_filepath='section_FCSV/KPI5.csv'):
    header_keywords = ['Month', 'Baked Namkeen (Mention Volume)', 'Fried Namkeen (Relative Interest)']
    actual_header_row = find_header_row(csv_filepath, header_keywords)
    if actual_header_row is None:
        return None, "Header not found"

    df = pd.read_csv(csv_filepath, header=actual_header_row, encoding='utf-8-sig')
    df.columns = df.columns.map(lambda x: str(x).strip() if pd.notna(x) else x)

    # Find the 'Month' column
    first_data_column_index = next((i for i, col in enumerate(df.columns) if col.strip() == 'Month'), None)
    if first_data_column_index is None or first_data_column_index + 7 > len(df.columns):
        return None, "Insufficient columns or 'Month' not found"

    df = df.iloc[:, first_data_column_index : first_data_column_index + 7].copy()
    df.columns = [
        'Month', 'Baked_SM_Volume', 'Baked_SM_Comment',
        'Fried_SM_Volume', 'Fried_SM_Comment',
        'Baked_GT_Interest', 'Fried_GT_Interest'
    ]

    df.dropna(subset=['Month'], how='all', inplace=True)
    df = df[df['Month'].astype(str).str.strip() != '']
    df['Month'] = pd.to_datetime(df['Month'], format='%b-%y', errors='coerce')
    df.dropna(subset=['Month'], inplace=True)

    for col in ['Baked_SM_Volume', 'Fried_SM_Volume', 'Baked_GT_Interest', 'Fried_GT_Interest']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=['Baked_SM_Volume', 'Fried_SM_Volume', 'Baked_GT_Interest', 'Fried_GT_Interest'], inplace=True)

    df['Baked_SM_Comment'] = df['Baked_SM_Comment'].astype(str)
    df['Fried_SM_Comment'] = df['Fried_SM_Comment'].astype(str)

    df.drop_duplicates(subset=['Month', 'Baked_SM_Volume', 'Fried_SM_Volume', 'Baked_GT_Interest', 'Fried_GT_Interest', 'Baked_SM_Comment', 'Fried_SM_Comment'], inplace=True)

    monthly_data = df.groupby('Month').agg(
        Avg_Baked_SM_Volume=('Baked_SM_Volume', 'mean'),
        Avg_Fried_SM_Volume=('Fried_SM_Volume', 'mean'),
        Avg_Baked_GT_Interest=('Baked_GT_Interest', 'mean'),
        Avg_Fried_GT_Interest=('Fried_GT_Interest', 'mean'),
    ).reset_index()
    monthly_data.sort_values('Month', inplace=True)

    # --- Plot Both Charts Together ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Google Trends Chart
    ax1.plot(monthly_data['Month'], monthly_data['Avg_Baked_GT_Interest'], label='Baked Namkeen (Google Trends)', marker='o', linestyle='-', color='royalblue')
    ax1.plot(monthly_data['Month'], monthly_data['Avg_Fried_GT_Interest'], label='Fried Namkeen (Google Trends)', marker='x', linestyle='--', color='orangered')
    ax1.set_title('Google Trends: Baked vs. Fried Namkeen (Relative Interest)', fontsize=14)
    ax1.set_ylabel('Average Relative Interest (0-100)')
    ax1.legend()
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

    # Social Media Volume Chart
    ax2.plot(monthly_data['Month'], monthly_data['Avg_Baked_SM_Volume'], label='Baked Namkeen (Social Media Vol.)', marker='s', linestyle='-', color='forestgreen')
    ax2.plot(monthly_data['Month'], monthly_data['Avg_Fried_SM_Volume'], label='Fried Namkeen (Social Media Vol.)', marker='^', linestyle='--', color='purple')
    ax2.set_title('Social Media: Baked vs. Fried Namkeen (Mention Volume)', fontsize=14)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Average Mention Volume')
    ax2.legend()
    ax2.grid(True, linestyle=':', alpha=0.7)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=100)
    plt.close()
    img_buffer.seek(0)

    return img_buffer, None

@app.get("/F/kpi5/charts")
def get_combined_chart():
    chart_buffer, error = analyze_subsegment_growth_robust('section_FCSV/KPI5.csv')
    if error:
        return Response(content=error, media_type="text/plain", status_code=400)
    return StreamingResponse(chart_buffer, media_type="image/png")
