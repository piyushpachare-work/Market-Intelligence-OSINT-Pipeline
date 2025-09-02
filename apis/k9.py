import pandas as pd
from fastapi import APIRouter
from typing import Dict
import traceback

router = APIRouter()

def convert_np_types(obj):
    import numpy as np
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

@router.get("/kpi/9")
def run_kpi_9(file_path: str = "Market_data/KPI-9.csv") -> Dict:
    try:
        df = pd.read_csv(file_path, skiprows=2)
        df.dropna(how='all', inplace=True)
        
        # Debug: check columns
        # print("Columns in CSV:", df.columns.tolist())

        total_entries = len(df)
        companies = df['Company'].dropna().unique().tolist() if 'Company' in df.columns else []
        activity_counts = df['Company'].value_counts().to_dict() if 'Company' in df.columns else {}
        activity_types = df['Activity Type'].value_counts().to_dict() if 'Activity Type' in df.columns else {}
        sentiment_summary = df['Sentiment'].value_counts().to_dict() if 'Sentiment' in df.columns else {}

        if 'Category' in df.columns:
            snack_related = df[df['Category'].str.contains("snack", case=False, na=False)]
            snack_count = snack_related.shape[0]
            snack_percentage = round((snack_count / total_entries) * 100, 1) if total_entries > 0 else 0
        else:
            snack_count = 0
            snack_percentage = 0

        descriptions = df['Description'].dropna().tolist() if 'Description' in df.columns else []
        notes = df['Additional Notes'].dropna().tolist() if 'Additional Notes' in df.columns else []
        combined_text = " ".join(descriptions + notes)
        sample_excerpt = combined_text[:400] + "..." if combined_text else "N/A"

        result = {
            "qualitative_summary": {
                "total_entries": total_entries,
                "companies_covered": companies,
                "activity_types": activity_types,
                "activity_counts_by_company": activity_counts,
                "snack_food_related_entries": {
                    "count": snack_count,
                    "percentage": snack_percentage
                },
                "sentiment_summary": sentiment_summary,
                "sample_themes_excerpt": sample_excerpt
            }
        }

        return convert_np_types(result)
    
    except Exception as e:
        print("❌ Exception occurred in KPI-9:")
        traceback.print_exc()
        return {"error": str(e)}
