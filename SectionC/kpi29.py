import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_qualitative_product_visibility_table():
    # Load the CSV file
    df = pd.read_csv("sectionCdata/launch_visibility.csv")

    # Define logic for qualitative assessment
    def assess_visibility(row):
        visibility = str(row['Overall Visibility']).strip().lower()
        remark = str(row['Remark']).strip().lower()
        if visibility == "high":
            return "High visibility within 1 week"
        elif visibility == "medium":
            return "Moderate visibility in early weeks"
        elif visibility == "poor":
            if "search" in remark or "only one" in remark:
                return "Low presence and slow rollout observed"
            return "Slow rollout observed"
        else:
            return "Assessment not clear"

    df['Qualitative Assessment'] = df.apply(assess_visibility, axis=1)
    table_df = df[['Product', 'Qualitative Assessment']]

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(8, len(table_df)*0.5 + 1))
    ax.axis('off')
    tbl = ax.table(cellText=table_df.values, colLabels=table_df.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.auto_set_column_width(col=list(range(len(table_df.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()