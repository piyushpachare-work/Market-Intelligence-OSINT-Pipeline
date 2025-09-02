# file: code/adv_comp/marketing_msg_consistency.py

import pandas as pd
import matplotlib.pyplot as plt
import io

def marketing_message_scores(csv_path: str = "data/Competitor Marketing Message Co.csv"):
    """
    Returns brand-level consistency scores as a list of dictionaries.
    """
    df = pd.read_csv(csv_path)
    df_clean = df[df['Consistency Score'].notna()]
    result = df_clean[['Brand', 'Consistency Score']].copy()
    result['Brand'] = result['Brand'].str.strip()
    result['Consistency Score'] = result['Consistency Score'].str.strip()
    return result.to_dict(orient="records")


def marketing_message_consistency_plot(csv_path: str = "data/Competitor Marketing Message Co.csv") -> bytes:
    """
    Returns a bar chart PNG showing the number of competitors by consistency level.
    """
    df = pd.read_csv(csv_path)
    df_clean = df[df['Consistency Score'].notna()].copy()
    
    # Normalize and categorize consistency levels
    df_clean['Consistency Level'] = df_clean['Consistency Score'].map({
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low'
    })

    consistency_count = df_clean.groupby('Consistency Level').size().reset_index(name='Competitor Count')

    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(consistency_count['Consistency Level'], consistency_count['Competitor Count'],
            color=['green', 'yellow', 'red'])
    plt.title('Competitor Marketing Message Consistency Level')
    plt.xlabel('Consistency Level')
    plt.ylabel('Number of Competitors')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()