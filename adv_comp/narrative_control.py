# file: code/adv_comp/narrative_control.py

import pandas as pd
import matplotlib.pyplot as plt
import io

def narrative_control_data(csv_path: str ="data/Competitor Narrative Control Sc.csv"):
    df = pd.read_csv(csv_path)
    narrative_mapping = {
        '🟠 Moderate': 'Moderate',
        '🔵 Strong': 'Strong'
    }
    df['Narrative Control Score'] = df['Narrative Control Score'].map(narrative_mapping)
    table = df[['Competitor', 'Narrative Control Score']].dropna().to_dict(orient='records')
    score_counts = df['Narrative Control Score'].value_counts()
    return {"table": table, "score_counts": score_counts.to_dict()}

def narrative_control_plot(csv_path: str = "data/Competitor Narrative Control Sc.csv"):
    df = pd.read_csv(csv_path)
    narrative_mapping = {
        '🟠 Moderate': 'Moderate',
        '🔵 Strong': 'Strong'
    }
    df['Narrative Control Score'] = df['Narrative Control Score'].map(narrative_mapping)
    score_counts = df['Narrative Control Score'].value_counts()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(score_counts.index, score_counts.values, color=['#FF5733', '#2980B9'])
    ax.set_title('Competitor Narrative Control Score Distribution', fontsize=14)
    ax.set_xlabel('Narrative Control Score', fontsize=12)
    ax.set_ylabel('Number of Competitors', fontsize=12)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()