import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_restaurant_presence_table():
    # Step 1: Read the CSV file
    df = pd.read_csv("sectionCdata/restaurant_presence.csv")

    # Step 2: Drop the 'Sources' column
    df_cleaned = df.drop(columns=['Sources'])

    # Step 3: Plot the cleaned DataFrame as an image
    fig, ax = plt.subplots(figsize=(8, len(df_cleaned)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=df_cleaned.values, colLabels=df_cleaned.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(df_cleaned.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()