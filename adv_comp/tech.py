import pandas as pd

def load_tech_adoption_summary():
    file_path = "data/Competitor Technology Adoption .csv"
    df = pd.read_csv(file_path)

    selected_cols = [
        'Company',
        'Glassdoor Rating',
        'Recommend to Friend',
        'Top Positives',
        'Top Negatives',
        'Tech Adoption Signals',
        'Tech Maturity',
        'Employer Branding Score'
    ]

    df_summary = df[selected_cols].dropna(subset=['Company']).copy()

    for emoji in ['🟠 ', '🔵 ', '🔴 ']:
        df_summary['Employer Branding Score'] = df_summary['Employer Branding Score'].str.replace(emoji, '', regex=False)

    # Convert dataframe to dict (records) for JSON serialization
    return df_summary.to_dict(orient='records')