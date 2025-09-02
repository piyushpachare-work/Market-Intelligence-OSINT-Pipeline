import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def load_and_clean_data(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=2)
        df.columns = [
            "Sr_No", "Date", "Investment_Type", "Investment_Amount", "Investor",
            "Company", "Sector", "Purpose", "Region", "Stage",
            "Strategic_Alignment", "Food_Sector_Impact", "Funding_Stage",
            "Key_People", "Partnerships", "Media_Source", "Impact_on_Haldiram",
            "Notes"
        ]

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=["Date", "Investment_Amount", "Company"])

        def parse_amount(amount):
            try:
                amount = amount.replace('$', '').replace(',', '').lower()
                if 'million' in amount:
                    return float(amount.replace('million', '').strip()) * 1_000_000
                elif 'billion' in amount:
                    return float(amount.replace('billion', '').strip()) * 1_000_000_000
                else:
                    return float(amount)
            except:
                return None

        df['Investment_Amount_Num'] = df['Investment_Amount'].apply(parse_amount)
        df = df.dropna(subset=["Investment_Amount_Num"])
        df = df.sort_values("Date")

        return df
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_timeline_chart_base64(df):
    try:
        plt.figure(figsize=(12, 6))
        plt.scatter(df['Date'], df['Investment_Amount_Num'], color='green', s=100)

        for i in range(len(df)):
            plt.text(df['Date'].iloc[i], df['Investment_Amount_Num'].iloc[i],
                     df['Company'].iloc[i], fontsize=9, ha='right', rotation=45)

        plt.title("📈 Timeline of Key Investment Events")
        plt.xlabel("Date")
        plt.ylabel("Investment Amount (USD)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    except Exception as e:
        print(f"Error generating timeline chart: {e}")
        return None


def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-7.csv")
    df = load_and_clean_data(file_path)

    if df is not None and not df.empty:
        chart_base64 = generate_timeline_chart_base64(df)

        timeline = [
            {
                "date": str(row["Date"].date()),
                "company": row["Company"],
                "investment_usd": round(row["Investment_Amount_Num"]),
                "investment_type": row["Investment_Type"]
            }
            for _, row in df.iterrows()
        ]

        return {
            "kpi_name": "Investment Timeline",
            "total_investments": len(df),
            "timeline": timeline,
            "chart_base64": chart_base64
        }

    else:
        return {
            "kpi_name": "Investment Timeline",
            "error": "No data available or failed to process"
        }
