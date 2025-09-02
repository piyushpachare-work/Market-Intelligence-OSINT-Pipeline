import pandas as pd

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-12.csv")
    df = pd.read_csv(file_path)
    trend_keywords = ['Rising', 'Stable', 'Volatile']
    trend_data = []
    for index, row in df.iterrows():
        for col in df.columns:
            cell = str(row[col])
            for trend in trend_keywords:
                if trend.lower() in cell.lower():
                    trend_data.append((row['Ingredient'] if 'Ingredient' in df.columns else row[col], trend))
                    break
    trend_df = pd.DataFrame(trend_data, columns=['Ingredient', 'Price Trend'])
    trend_df = trend_df.drop_duplicates().sort_values(by='Ingredient')
    summary = trend_df['Price Trend'].value_counts().to_dict()
    return {
        "kpi_name": "Price Trend Mentions by Ingredient",
        "trend_summary": summary,
        "total_ingredients": trend_df['Ingredient'].nunique()
    }