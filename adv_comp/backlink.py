import pandas as pd
from fastapi.responses import JSONResponse

def process_backlink_data(csv_path: str):
    def convert_backlinks(value):
        if isinstance(value, str):
            value = value.strip()
            if 'K' in value:
                return float(value.replace('K', '').strip()) * 1e3
            elif 'M' in value:
                return float(value.replace('M', '').strip()) * 1e6
            else:
                return float(value)
        elif pd.isna(value):
            return 0.0
        else:
            return float(value)

    def assess_backlink_quality(row):
        if (row['DOMAIN RATING'] > 45 and row['BACKLINKS'] > 10000 and row['LINKING WEBSITES'] > 500):
            return 'Strong'
        elif (35 <= row['DOMAIN RATING'] <= 45 and 1000 <= row['BACKLINKS'] <= 10000 and 200 <= row['LINKING WEBSITES'] <= 500):
            return 'Moderate'
        else:
            return 'Weak'

    df = pd.read_csv(csv_path)
    df['DOMAIN RATING'] = pd.to_numeric(df['DOMAIN RATING'], errors='coerce').fillna(0)
    df['BACKLINKS'] = df['BACKLINKS'].apply(convert_backlinks)
    df['LINKING WEBSITES'] = df['LINKING WEBSITES'].apply(convert_backlinks)
    df['BACKLINK_QUALITY'] = df.apply(assess_backlink_quality, axis=1)
    # Replace NaN and inf values before returning
    safe_df = df[['Brand', 'BACKLINK_QUALITY']].replace([float('inf'), float('-inf')], None)
    safe_df = safe_df.where(pd.notnull(safe_df), None)
    return safe_df

# === API function ===
def backlink_endpoint():
    csv_path = "data/Competitor Website Backlink Qua.csv"
    result_df = process_backlink_data(csv_path)
    return JSONResponse(content=result_df.to_dict(orient="records"))