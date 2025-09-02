import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for FastAPI/server

import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_total_reviews_table():
    # Read CSVs with default header (header=0)
    data_dining = pd.read_csv("sectionCdata/Online Review Volume - Restaurants.csv")
    data_products = pd.read_csv("sectionCdata/Online Review Volume - Products.csv")

    # Clean column names
    data_dining.columns = data_dining.columns.str.strip()
    data_products.columns = data_products.columns.str.strip()

    # Use the exact column name
    total_dining = data_dining["No. of Reviews"].sum()
    total_delivery = data_products["No. of Reviews"].sum()
    estimated_total = total_dining + total_delivery

    # Prepare a DataFrame for display
    df = pd.DataFrame({
        "Category": ["Dining Reviews", "Delivery Reviews", "Estimated Total Reviews"],
        "Count": [total_dining, total_delivery, estimated_total]
    })

    # Plot the table as an image
    fig, ax = plt.subplots(figsize=(6, 2.5))
    ax.axis('off')
    tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.auto_set_column_width(col=list(range(len(df.columns))))
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()