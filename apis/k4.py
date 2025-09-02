import pandas as pd
from pathlib import Path
import numpy as np
import json

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
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.generic,)):  # Catch all NumPy scalars
        return obj.item()
    else:
        return obj

def run_kpi(params=None):
    try:
        file_path = Path("Market_data/KPI-4.csv")
        df = pd.read_csv(file_path, skiprows=2)

        expected_cols = ['Sr_No', 'Date', 'Category', 'Search_Term', 'Relative_Interest', 'Platform_Link']
        if len(df.columns) == len(expected_cols):
            df.columns = expected_cols
        else:
            return {"error": "Unexpected number of columns in KPI-4.csv"}

        df = df.dropna(subset=['Date', 'Category', 'Relative_Interest'])
        if df.empty:
            return {"error": "No valid data found after cleaning."}

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df = df.sort_values('Date')

        summary_df = df.groupby('Category')['Relative_Interest'].agg(['mean', 'max', 'min', 'count']).round(1)
        summary = summary_df.reset_index().to_dict(orient='records')

        recent_cutoff = pd.Timestamp.now() - pd.DateOffset(months=6)
        recent = df[df['Date'] >= recent_cutoff]

        recent_avg = {}
        if not recent.empty:
            recent_avg = recent.groupby('Category')['Relative_Interest'].mean().round(1).to_dict()

        trend_direction = []
        for category in df['Category'].unique():
            cat_data = df[df['Category'] == category].tail(12)
            if len(cat_data) > 1:
                start = cat_data['Relative_Interest'].iloc[0]
                end = cat_data['Relative_Interest'].iloc[-1]
                trend = "Rising 📈" if end > start else "Declining 📉"
                change = round(end - start, 1)
                trend_direction.append({
                    "category": category,
                    "trend": trend,
                    "change_points": change
                })

        peak_performance = []
        for category in df['Category'].unique():
            cat_data = df[df['Category'] == category]
            if not cat_data.empty:
                idxmax = cat_data['Relative_Interest'].idxmax()
                peak = cat_data.loc[idxmax]
                peak_performance.append({
                    "category": category,
                    "peak_interest": peak['Relative_Interest'],
                    "peak_month": peak['Date'].strftime('%Y-%m')
                })

        if summary_df.empty or not recent_avg:
            key_insights = {}
        else:
            strongest = summary_df['mean'].idxmax()
            most_volatile = (summary_df['max'] - summary_df['min']).idxmax()
            fastest_growing = max(recent_avg, key=recent_avg.get)

            key_insights = {
                "strongest_overall_trend": {
                    "category": strongest,
                    "avg_score": summary_df.loc[strongest, 'mean']
                },
                "most_volatile": most_volatile,
                "currently_hottest": {
                    "category": fastest_growing,
                    "recent_avg_score": recent_avg[fastest_growing]
                }
            }

        result = {
            "total_records": len(df),
            "summary_by_category": summary,
            "recent_average_interest": recent_avg,
            "trend_direction": trend_direction,
            "peak_performance": peak_performance,
            "key_insights": key_insights
        }

        # ✅ Convert to native Python types
        result = convert_np_types(result)

        # ✅ Optional: simulate JSON serialization for debugging
        try:
            json.dumps(result)
        except TypeError as e:
            print("Serialization error:", e)

        return result

    except Exception as e:
        return {"error": str(e)}
