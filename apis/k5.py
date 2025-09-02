import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
import traceback

def convert_np_types(obj):
    if isinstance(obj, dict):
        return {k: convert_np_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_np_types(i) for i in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Period):
        return str(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.generic,)):
        return obj.item()
    else:
        return obj

def run_kpi(params):
    try:
        file_path = params.get("file_path", "Market_data/KPI-5.csv")
        df = pd.read_csv(file_path, skiprows=3)
        df.columns = ['Sr. No.', 'Date', 'Regulatory Change', 'Category', 'Impact Area', 'News Frequency', 'Platform Link']
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Quarter'] = df['Date'].dt.to_period('Q')
        df['Year'] = df['Date'].dt.year
        quarterly_counts = df.groupby('Quarter').size().reset_index(name='Event Count')
        quarterly_counts['Quarter'] = quarterly_counts['Quarter'].astype(str)

        result = {
            "description": "Regulatory Events / News Mentions per Quarter",
            "data_points": quarterly_counts.to_dict(orient="records")
        }
        return convert_np_types(result)
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

def get_plot_image(file_path):
    file_path = file_path or "Market_data/KPI-5.csv"
    df = pd.read_csv(file_path, skiprows=3)
    df.columns = ['Sr. No.', 'Date', 'Regulatory Change', 'Category', 'Impact Area', 'News Frequency', 'Platform Link']
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df['Quarter'] = df['Date'].dt.to_period('Q')
    quarterly_counts = df.groupby('Quarter').size().reset_index(name='Event Count')
    quarterly_counts['Quarter'] = quarterly_counts['Quarter'].astype(str)

    plt.figure(figsize=(10, 6))
    plt.plot(quarterly_counts['Quarter'], quarterly_counts['Event Count'], marker='o', linestyle='-')
    plt.title('Regulatory Events / News Mentions per Quarter')
    plt.xlabel('Quarter')
    plt.ylabel('Number of Events')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf