from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import io
import numpy as np

app = FastAPI()

@app.get("/F/kpi6/chart")
def get_disruption_chart():
    csv_filepath = 'section_FCSV/KPI6.csv'

    try:
        df = pd.read_csv(csv_filepath, usecols=range(5), encoding='utf-8')
    except:
        return Response(content="Failed to read the CSV", status_code=500)

    # Clean column names
    if df.columns[0].startswith('\ufeff'):
        df.columns.values[0] = df.columns[0].replace('\ufeff', '')

    expected_headers = ['Date', 'Description', 'Impact_Area', 'Source_Type', 'Severity']
    df.columns = expected_headers[:len(df.columns)]

    if 'Date' not in df.columns or 'Description' not in df.columns:
        return Response(content="Missing required columns", status_code=400)

    if 'Severity' not in df.columns:
        df['Severity'] = 'N/A'
    else:
        df['Severity'] = df['Severity'].astype(str).str.strip().fillna('N/A')

    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df.dropna(subset=['Date', 'Description'], inplace=True)
    df.sort_values('Date', inplace=True)

    if df.empty:
        return Response(content="No valid data", status_code=204)

    # Plot details
    severity_map = {
        'High': {'color': 'red', 'level_factor': 1.0, 'size': 80},
        'Medium': {'color': 'orange', 'level_factor': 0.7, 'size': 50},
        'Low': {'color': 'green', 'level_factor': 0.4, 'size': 30},
        'N/A': {'color': 'grey', 'level_factor': 0.2, 'size': 20}
    }

    df['Plot_Color'] = df['Severity'].apply(lambda x: severity_map.get(x, severity_map['N/A'])['color'])
    df['Plot_Level_Factor'] = df['Severity'].apply(lambda x: severity_map.get(x, severity_map['N/A'])['level_factor'])
    df['Plot_Size'] = df['Severity'].apply(lambda x: severity_map.get(x, severity_map['N/A'])['size'])

    base_levels = np.tile([1.5, -1.5, 1.2, -1.2, 0.9, -0.9, 0.6, -0.6], int(np.ceil(len(df.index)/8)))[:len(df.index)]
    df['Text_Y_Position'] = base_levels * df['Plot_Level_Factor']

    # Plotting
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(18, 9), constrained_layout=True)

    ax.axhline(0, color='black', linewidth=0.5)

    for _, row in df.iterrows():
        ax.plot([row['Date'], row['Date']], [0, row['Text_Y_Position']], color='grey', linestyle='-', linewidth=0.7)
        ax.plot(row['Date'], row['Text_Y_Position'], marker='o', color=row['Plot_Color'], 
                markersize=np.sqrt(row['Plot_Size'])/1.5, markeredgecolor='black', mew=0.5)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    ax.set_title('Supply Chain Disruption Timeline', fontsize=18, pad=20)
    ax.yaxis.set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines['bottom'].set_position(('data', 0))

    min_y = df['Text_Y_Position'].min()
    max_y = df['Text_Y_Position'].max()
    ax.set_ylim(min_y - 0.15 * abs(min_y), max_y + 0.15 * abs(max_y))

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=sev, 
               markerfacecolor=details['color'], markersize=np.sqrt(details['size'])/2)
        for sev, details in severity_map.items()
    ]
    ax.legend(handles=legend_elements, title="Severity", loc='lower left', fontsize=8)

    # Return image as response
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120)
    plt.close(fig)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
