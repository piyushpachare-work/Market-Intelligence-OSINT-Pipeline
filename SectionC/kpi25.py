import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_negative_reviews_bar():
    data = pd.read_csv("sectionCdata/negative_reviews.csv")
    labels = data.iloc[:, 0]
    values = data.iloc[:, 1]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color='salmon')
    plt.xlabel(data.columns[0])
    plt.ylabel(data.columns[1])
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Bar Chart of {data.columns[0]} vs {data.columns[1]}")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()