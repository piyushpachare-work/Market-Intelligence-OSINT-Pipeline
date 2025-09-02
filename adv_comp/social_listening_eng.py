import pandas as pd
import re

FILE_PATH = "data/Competitor Social Listening Eng.csv"

def remove_emojis(text):
    if pd.isna(text):
        return ""
    return re.sub(r'[^\w\s\-\/&]', '', str(text)).strip()

def classify_engagement(tendency):
    tendency_lower = tendency.lower()
    if 'active' in tendency_lower or 'monitoring' in tendency_lower:
        return 'Active'
    elif 'passive' in tendency_lower or 'opportunistic' in tendency_lower or 'reactive' in tendency_lower:
        return 'Passive'
    elif 'no' in tendency_lower or 'silent' in tendency_lower:
        return 'None'
    else:
        return 'Unknown'

def load_and_process_engagement():
    df = pd.read_csv(FILE_PATH)

    df['Overall Tendency'] = df['Overall Tendency'].apply(remove_emojis)
    df['Engagement Category'] = df['Overall Tendency'].apply(classify_engagement)

    output_df = df[['Brand', 'Engagement Category']]
    output_df = output_df[output_df['Brand'].notna() & output_df['Brand'].str.strip().ne('')]

    # Convert to list of dicts for JSON response
    return output_df.to_dict(orient='records')