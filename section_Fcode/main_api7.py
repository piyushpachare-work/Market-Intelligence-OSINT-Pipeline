from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

app = FastAPI()

def generate_kpi7_plot(csv_filepath='section_FCSV/KPI7.csv'):
    try:
        with open(csv_filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

        header_row_index = -1
        for i, line in enumerate(lines):
            if "Month-Year" in line and "Total Price Mentions" in line:
                header_row_index = i
                break

        if header_row_index == -1:
            return None, "Header row not found"

        df = pd.read_csv(csv_filepath, header=header_row_index, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()

        required_cols = ['Month-Year', 'Total Price Mentions', '% Negative Price Mentions', 'Notes/Events']
        for col in required_cols:
            if col not in df.columns:
                return None, f"Missing column: {col}"

        df = df[required_cols].dropna(subset=['Month-Year'])
        df = df[df['Month-Year'].str.contains('-', na=False)]

        df['Date'] = pd.to_datetime(df['Month-Year'], format='%b-%y', errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        df['Total Price Mentions'] = pd.to_numeric(df['Total Price Mentions'], errors='coerce')
        df['% Negative Price Mentions'] = pd.to_numeric(df['% Negative Price Mentions'].astype(str).str.rstrip('%'), errors='coerce')
        df.dropna(subset=['Total Price Mentions', '% Negative Price Mentions'], inplace=True)

        df.sort_values('Date', inplace=True)

        plt.style.use('seaborn-v0_8-whitegrid')
        fig, ax1 = plt.subplots(figsize=(14, 7))

        color1 = 'tab:blue'
        ax1.set_xlabel('Month-Year')
        ax1.set_ylabel('Total Price Mentions', color=color1)
        ax1.plot(df['Date'], df['Total Price Mentions'], color=color1, marker='o', linestyle='-', label='Total Price Mentions')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, linestyle=':', alpha=0.7)

        ax2 = ax1.twinx()
        color2 = 'tab:red'
        ax2.set_ylabel('% Negative Price Mentions', color=color2)
        ax2.plot(df['Date'], df['% Negative Price Mentions'], color=color2, marker='x', linestyle='--', label='% Negative Price Mentions')
        ax2.tick_params(axis='y', labelcolor=color2)

        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
        plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

        fig.suptitle('Price Sensitivity Fluctuation Over Time')
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', dpi=100)
        plt.close(fig)
        buffer.seek(0)

        return buffer, None
    except Exception as e:
        return None, str(e)

@app.get("/F/kpi7/plot")
def kpi7_plot():
    plot_buffer, error = generate_kpi7_plot()
    if error:
        return {"error": error}
    return StreamingResponse(plot_buffer, media_type="image/png")
