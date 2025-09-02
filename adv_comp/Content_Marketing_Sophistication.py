import pandas as pd
import re
from fastapi.responses import JSONResponse

def process_content_marketing(csv_path: str):
    df = pd.read_csv(csv_path)

    def remove_emojis(text):
        if pd.isna(text):
            return ""
        return re.sub(r'[^\w\s\-\/]', '', str(text)).strip()

    df['Sophistication Level'] = df['Sophistication Level'].apply(remove_emojis)
    df['Sophistication Level'] = df['Sophistication Level'].str.replace("Basic to Moderate", "Basic", regex=False)

    output_df = df[['Brand', 'Sophistication Level']]
    return output_df

def content_marketing_endpoint():
    csv_path = "data/Competitor Content Marketing So.csv"
    result_df = process_content_marketing(csv_path)
    return JSONResponse(content=result_df.to_dict(orient="records"))