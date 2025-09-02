import pandas as pd
import matplotlib.pyplot as plt

def extract_kpi_data(file_path):
    try:
        df = pd.read_csv(file_path, header=None)

        start_row = None
        for i in range(len(df)):
            if "Sr No" in df.iloc[i].values:
                start_row = i
                break

        if start_row is None:
            return None

        header = df.iloc[start_row].tolist()
        data = df.iloc[start_row + 1:].values.tolist()
        extracted_df = pd.DataFrame(data, columns=header)

        extracted_df = extracted_df.dropna(subset=['Category', 'Brand', 'Date', 'Estimated Market Size (₹ Cr)', 'CAGR (%)'])
        extracted_df['Estimated Market Size (₹ Cr)'] = pd.to_numeric(extracted_df['Estimated Market Size (₹ Cr)'], errors='coerce')
        extracted_df['CAGR (%)'] = pd.to_numeric(extracted_df['CAGR (%)'], errors='coerce')
        extracted_df = extracted_df.dropna(subset=['Estimated Market Size (₹ Cr)', 'CAGR (%)'])

        return extracted_df

    except Exception as e:
        print(f"Error: {e}")
        return None

def summarize_kpi_data(df):
    if df is None or df.empty:
        return None

    summary_df = df.groupby('Category')[['Estimated Market Size (₹ Cr)', 'CAGR (%)']].mean()
    summary_df = summary_df.sort_values(by='Estimated Market Size (₹ Cr)', ascending=False)
    summary_df = summary_df.reset_index()
    return summary_df

# ✅ This function is called by FastAPI
def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-1.csv")  # default fallback
    df = extract_kpi_data(file_path)
    summary_df = summarize_kpi_data(df)

    if summary_df is not None:
        result = summary_df.to_dict(orient="records")
        return {
            "kpi_name": "Market Size Summary",
            "data": result,
            "unit": "INR Cr"
        }
    else:
        return {
            "kpi_name": "Market Size Summary",
            "data": [],
            "error": "No data found or processed"
        }