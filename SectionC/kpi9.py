import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_posting_frequency_table():
    # Load the posting frequency CSV
    df = pd.read_csv('sectionCdata/_Posting_Frequency.csv')

    # Sort the brands by posts in descending order
    df_sorted = df.sort_values(by='Posts in Last 30 Days', ascending=False)

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(8, len(df_sorted)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=df_sorted.values, colLabels=df_sorted.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(df_sorted.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()