import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_follower_count_table():
    # Load the data
    df = pd.read_csv("sectionCdata/follower_count.csv")

    # Function to convert '22.7K' or '156k' to numbers like 22700, 156000
    def convert_to_number(x):
        x = str(x).strip().lower()
        if 'k' in x:
            return float(x.replace('k', '')) * 1000
        try:
            return float(x)
        except:
            return 0

    # Apply conversion to follower count columns (all except first 'Company')
    for col in df.columns[1:]:
        df[col] = df[col].apply(convert_to_number)

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