import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
from io import BytesIO

def generate_breadth_plot():
    # === Step 1: Define CSV file paths ===
    category_files = {
        'Namkeen': 'data/SKU NAMKEEN.csv',
        'Sweets': 'data/SKU SWEETS.csv',
        'Frozen Foods': 'data/SKU FROZEN FOODS.csv',
        'Biscuits': 'data/SKU BISCUITS.csv',
        'RTE': 'data/SKU RTE.csv',
        'Chips': 'data/SKU CHIPS.csv'
    }

    # === Step 2: Dictionary to track category presence per brand ===
    brand_categories = defaultdict(set)

    # === Step 3: Read each file and update brand's category set ===
    for category, file_path in category_files.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if 'Brand' in df.columns:
                    for brand in df['Brand'].dropna().unique():
                        brand_categories[brand.strip()].add(category)
            except Exception:
                continue

    # === Step 4: Prepare final data ===
    breadth_data = {
        'Brand': [],
        'Category Breadth': []
    }

    for brand, categories in brand_categories.items():
        breadth_data['Brand'].append(brand)
        breadth_data['Category Breadth'].append(len(categories))

    df_breadth = pd.DataFrame(breadth_data)
    df_breadth = df_breadth.sort_values(by='Category Breadth', ascending=False)

    # === Step 5: Plotting ===
    plt.figure(figsize=(12, 6))
    bars = plt.bar(df_breadth['Brand'], df_breadth['Category Breadth'], color='royalblue')

    # Optional: Highlight Haldiram's in a different color
    for bar, brand in zip(bars, df_breadth['Brand']):
        if "Haldiram" in brand:
            bar.set_color('orange')

    plt.title('Product Category Breadth: Haldiram vs Competitors', fontsize=14)
    plt.xlabel('Brand', fontsize=12)
    plt.ylabel('Number of Categories', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf