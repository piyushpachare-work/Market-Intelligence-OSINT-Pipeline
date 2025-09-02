import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_page_speed_table():
    # Read the CSV file
    df = pd.read_csv('sectionCdata/page_speed_insight.csv')

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(8, len(df)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(df.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()