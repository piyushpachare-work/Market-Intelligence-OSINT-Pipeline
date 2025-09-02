import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_range_depth_plot():
    # === Step 1: Load your dataset ===
    file_path = 'data/Range Depth .csv'  # Update if your file name/path is different
    df = pd.read_csv(file_path)

    # === Step 2: Set the brand column as the index for better plotting ===
    df.set_index('Brand', inplace=True)

    # === Step 3: Plot SKU counts per category for all brands ===
    plt.figure(figsize=(16, 8))  # Wide figure for better readability
    df.plot(kind='bar', stacked=False, colormap='tab20', figsize=(16, 8))

    plt.title('SKU Count by Product Category for Haldiram vs Competitors', fontsize=16)
    plt.xlabel('Brand', fontsize=13)
    plt.ylabel('Number of SKUs', fontsize=13)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Product Category')
    plt.tight_layout()

    # === Step 4: Save and display ===
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf