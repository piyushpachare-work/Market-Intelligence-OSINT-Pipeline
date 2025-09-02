import pandas as pd

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-14.csv")
    df = pd.read_csv(file_path)
    df_cleaned = df.iloc[3:].copy()
    df_cleaned.columns = [
        'Emerging Category', 'Description', 'Rationale',
        'Industry Source/Report', 'Projected Growth (%)', 'Key Trends/Insights'
    ]
    df_cleaned.dropna(subset=['Emerging Category', 'Rationale'], inplace=True)
    rationale_summary = df_cleaned[['Emerging Category', 'Rationale']].to_dict(orient="records")
    return {
        "kpi_name": "Emerging Category Rationale",
        "summary": rationale_summary
    }