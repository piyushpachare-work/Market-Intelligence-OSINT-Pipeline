import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_response_rate_table():
    data = pd.read_csv("sectionCdata/response_rate.csv")
    data.columns = data.columns.str.strip()

    # Calculate response rate for each row
    data["Response Rate (%)"] = (data["No. of Responses"] / data["No. of Reviews Checked"]) * 100
    data["Response Rate (%)"] = data["Response Rate (%)"].round(2)

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(8, len(data)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(data.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()