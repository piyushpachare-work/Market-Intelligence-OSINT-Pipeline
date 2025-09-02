import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_bounce_rate_table():
    # Load the CSV file
    df = pd.read_csv('sectionCdata/bounce_name.csv')

    # Select only Brand and Bounce Rate (%) columns (preserve original order)
    bounce_df = df[['Brand', 'Bounce Rate (%)']]

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(6, len(bounce_df)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=bounce_df.values, colLabels=bounce_df.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(bounce_df.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()