# file: code/adv_comp/LitigationRegulatory.py

import pandas as pd
import matplotlib.pyplot as plt
import io

def litigation_issue_data(csv_path: str = "data/Competitor LitigationRegulatory.csv"):
    """
    Processes the litigation/regulatory issues CSV and returns the issue count per brand.

    Args:
        csv_path (str): Path to the litigation CSV file.

    Returns:
        List[dict]: List of brands with their issue counts.
    """
    df = pd.read_csv(csv_path)
    df_clean = df[df['Severity'].notna()]
    issue_count = df_clean.groupby('Brand').size().reset_index(name='Issue Count')
    return issue_count.to_dict(orient='records')


def litigation_issue_plot(csv_path: str = "data/Competitor LitigationRegulatory.csv") -> bytes:
    """
    Generates a bar chart for legal/regulatory issues per competitor.

    Args:
        csv_path (str): Path to the litigation CSV file.

    Returns:
        bytes: PNG image bytes of the bar chart.
    """
    df = pd.read_csv(csv_path)
    df_clean = df[df['Severity'].notna()]
    issue_count = df_clean.groupby('Brand').size().reset_index(name='Issue Count')

    plt.figure(figsize=(10, 6))
    plt.bar(issue_count['Brand'], issue_count['Issue Count'], color='skyblue')
    plt.title('Significant Legal/Regulatory Issues per Competitor')
    plt.xlabel('Competitor')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()