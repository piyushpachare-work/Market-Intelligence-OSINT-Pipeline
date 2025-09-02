# file: code/adv_comp/leadership_visibility.py

import pandas as pd

def leadership_visibility_endpoint(csv_path: str = "data/Competitor Leadership Visibilit.csv"):
    """
    Extracts and cleans leadership visibility data for each competitor.
    
    Args:
        csv_path (str): Path to the CSV containing visibility data.
    
    Returns:
        List[dict]: List of competitors with their visibility level and focus.
    """
    df = pd.read_csv(csv_path)

    # Drop rows missing required columns
    df.dropna(subset=['Competitor', 'Visibility Level & Focus'], inplace=True)

    # Select and clean relevant columns
    df = df[['Competitor', 'Visibility Level & Focus']]
    df['Competitor'] = df['Competitor'].str.strip()
    df['Visibility Level & Focus'] = df['Visibility Level & Focus'].str.strip()

    return df.to_dict(orient='records')