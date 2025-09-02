import pandas as pd

def get_marketing_campaigns():
    file_path = "data/Competitor Marketing Campaign I.csv"
    df_campaigns = pd.read_csv(file_path)
    df_campaigns.dropna(subset=['Competitor', 'Identified Marketing Campaigns'], inplace=True)
    competitor_campaigns = df_campaigns.groupby('Competitor').agg({
        'Identified Marketing Campaigns': lambda x: ', '.join(x)
    }).reset_index()
    return competitor_campaigns.to_dict(orient="records")