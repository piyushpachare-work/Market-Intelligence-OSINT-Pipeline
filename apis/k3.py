import pandas as pd
import matplotlib.pyplot as plt

def extract_kpi_data(file_path):
    try:
        df = pd.read_csv(file_path, header=None, skiprows=5)  # Skip initial blank rows

        # Find the row where actual data starts (look for "Entry ID")
        start_row = None
        for i in range(len(df)):
            if "Entry ID" in df.iloc[i].values:
                start_row = i
                break

        if start_row is None:
            return None

        # Extract header row and data
        header = df.iloc[start_row].tolist()
        data = df.iloc[start_row + 1:].values.tolist()
        extracted_df = pd.DataFrame(data, columns=header)

        # Drop rows with missing key columns
        extracted_df = extracted_df.dropna(subset=['Trend Category', 'Description', 'Source', 'Date Identified', 'Source URL'])
        return extracted_df

    except Exception:
        return None

def summarize_trend_categories(df):
    if df is None or df.empty:
        return None
    trend_counts = df['Trend Category'].value_counts().reset_index()
    trend_counts.columns = ['Trend Category', 'Count']
    trend_counts = trend_counts.sort_values('Count', ascending=False)
    return trend_counts

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-3.csv")
    df = extract_kpi_data(file_path)

    if df is None or df.empty:
        return {"kpi_name": "Key Market Trends", "error": "No data extracted from file."}

    trend_counts = summarize_trend_categories(df)
    if trend_counts is None or trend_counts.empty:
        return {"kpi_name": "Key Market Trends", "error": "No trend category summary available."}

    top_trend = trend_counts.iloc[0]
    trends_list = trend_counts.to_dict(orient="records")

    return {
        "kpi_name": "Key Market Trends",
        "top_trend_category": top_trend['Trend Category'],
        "mentions": int(top_trend['Count']),
        "total_trend_categories": len(trend_counts),
        "trend_categories_summary": trends_list
    }
