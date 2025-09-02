import pandas as pd

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-13.csv")
    df = pd.read_csv(file_path)
    df_cleaned = df.iloc[3:].copy()
    df_cleaned.columns = ['Region/City', 'Search Term', 'Relative Search Interest']
    df_cleaned.dropna(inplace=True)
    df_cleaned['Relative Search Interest'] = pd.to_numeric(df_cleaned['Relative Search Interest'], errors='coerce')
    df_cleaned.dropna(subset=['Relative Search Interest'], inplace=True)
    avg_interest = df_cleaned.groupby('Region/City')['Relative Search Interest'].mean().sort_values(ascending=False).reset_index()
    top_regions = avg_interest.head(10).to_dict(orient="records")
    return {
        "kpi_name": "Relative Search Interest by Region",
        "top_regions": top_regions
    }