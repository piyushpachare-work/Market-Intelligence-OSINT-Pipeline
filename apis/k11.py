import pandas as pd
import matplotlib.pyplot as plt
import io

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-11.csv")
    try:
        df = pd.read_csv(file_path, skiprows=2)
        df.dropna(how='all', inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        if df.empty:
            return {
                "kpi_name": "Q-commerce Activity Trend",
                "Total Entries": 0,
                "Tracked Quarters": [],
                "Activity Counts per Quarter": {},
                "message": "No valid data found in CSV."
            }

        df['Quarter'] = df['Date'].dt.to_period('Q')
        quarterly_trend = df.groupby('Quarter').size()

        summary = {
            "kpi_name": "Q-commerce Activity Trend",
            "Total Entries": len(df),
            "Tracked Quarters": quarterly_trend.index.astype(str).tolist(),
            "Activity Counts per Quarter": {str(k): int(v) for k, v in quarterly_trend.items()}
        }
        return summary

    except FileNotFoundError:
        return {"error": "CSV file not found."}
    except pd.errors.ParserError:
        return {"error": "Error parsing CSV file."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


def get_plot_image(file_path="Market_data/KPI-11.csv"):
    try:
        df = pd.read_csv(file_path, skiprows=2)
        df.dropna(how='all', inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])

        if df.empty:
            raise ValueError("No valid data found in CSV to plot.")

        df['Quarter'] = df['Date'].dt.to_period('Q')
        quarterly_trend = df.groupby('Quarter').size()

        plt.figure(figsize=(10, 5))
        quarterly_trend.plot(kind='line', marker='o', linestyle='-', color='green')
        plt.title('Q-commerce Activity Trend (Quarterly)')
        plt.xlabel('Quarter')
        plt.ylabel('Number of Activities')
        plt.grid(True)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return buf

    except FileNotFoundError:
        raise FileNotFoundError("CSV file not found.")
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while generating plot: {str(e)}")
