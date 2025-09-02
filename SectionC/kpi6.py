import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_kpi6_pie():
    df = pd.read_csv("sectionCdata/competitors_share_of_search.csv")
    plt.figure(figsize=(6, 6))
    plt.pie(df['Estimated Mentions'], labels=df['Brand'], autopct='%1.1f%%', startangle=140)
    plt.title("Social Media Share of Voice (Pie Chart)", fontsize=14)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()

