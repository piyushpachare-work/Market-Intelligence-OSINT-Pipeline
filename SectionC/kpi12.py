import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_traffic_estimate_table():
    # Load the CSV file
    df = pd.read_csv('sectionCdata/_Traffic_Estimate_Rank.csv')

    # Select relevant columns
    table = df[['Brand', 'Monthly Visits', 'Global Rank']]

    # Sort by Global Rank (ignoring missing values)
    table_sorted = table.sort_values(by='Global Rank', na_position='last')

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(8, len(table_sorted)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=table_sorted.values, colLabels=table_sorted.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(table_sorted.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()