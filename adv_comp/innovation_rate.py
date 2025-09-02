# file: code/adv_comp/innovation_rate.py

import pandas as pd

def innovation_rate_endpoint(csv_path: str = "data/Innovation Rate Proxy.csv"):
    """
    Processes innovation rate data from a CSV file and returns structured KPI results.
    
    Args:
        csv_path (str): Path to the CSV file containing new product launch data.
        
    Returns:
        List[dict]: List of dictionaries with competitor name, period, and launch count.
    """
    df = pd.read_csv(csv_path)

    # Clean data
    df.dropna(subset=["Competitor Name", "New Product Launches"], inplace=True)

    # Static period tagging (customize if needed)
    df['Period'] = 'Q1 2025'

    # Group and count product launches
    innovation_counts = (
        df.groupby(["Competitor Name", "Period"])
        .size()
        .reset_index(name='New Variant/Flavor Launches')
    )

    return innovation_counts.to_dict(orient="records")