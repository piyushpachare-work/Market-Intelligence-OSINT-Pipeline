import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse

def process_emp_rating(csv_path: str) -> pd.DataFrame:
    # Load CSV file
    df = pd.read_csv(csv_path)

    # Remove emojis from 'Branding Score', keep only Strong, Moderate, Weak
    df['Branding Score'] = df['Branding Score'].astype(str).str.extract(r'(Strong|Moderate|Weak)', expand=False)

    # Select only needed columns and drop rows where 'Competitor' is missing
    df = df[['Competitor', 
             'Overall Rating', 
             'CEO Approval', 
             'Recommend to Friend', 
             'Top Positives', 
             'Top Negatives', 
             'Branding Score']]
    
    df = df.dropna(subset=['Competitor'])

    return df

async def emp_rating_endpoint():
    csv_path = "data/Competitor Employer Branding Sc.csv"
    df = process_emp_rating(csv_path)

    # Robustly replace NaN, inf, -inf with None for all columns
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.astype(object).where(pd.notnull(df), None)

    return JSONResponse(content=df.to_dict(orient='records'))