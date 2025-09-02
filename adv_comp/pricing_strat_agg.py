import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Load the dataset
df = pd.read_csv("data/Competitor Pricing Strategy Agg.csv")

# Check column names
# print("Columns in dataset:", df.columns)  # <-- Commented out

# Clean data: Remove rows with missing values in 'Aggressiveness' column
df_clean = df[df['Aggressiveness'].notna()]

# Show the table with brand and aggressiveness score
brand_aggressiveness_table = df_clean[['Brand', 'Aggressiveness']]
# print("\nBrand and Aggressiveness Score Table:\n", brand_aggressiveness_table)  # <-- Commented out

# Map the aggressiveness levels to a categorical variable for consistency in the chart
df_clean['Aggressiveness Level'] = df_clean['Aggressiveness'].map({
    'High': 'High',
    'Medium': 'Medium',
    'Low': 'Low'
})

def get_pricing_aggressiveness_table():
    """
    Returns the cleaned brand aggressiveness table as list of dicts for API.
    """
    return brand_aggressiveness_table.to_dict(orient='records')

def get_pricing_aggressiveness_plot():
    """
    Returns the pricing aggressiveness bar chart as PNG bytes for API.
    """
    plt.figure(figsize=(10, 6))
    colors = ['green' if level == 'High' else 'yellow' if level == 'Medium' else 'red' for level in df_clean['Aggressiveness Level']]
    plt.bar(df_clean['Brand'], df_clean['Aggressiveness Level'].map({'High':3, 'Medium':2, 'Low':1}), color=colors)
    plt.title('Competitor Pricing Strategy Aggressiveness Level')
    plt.xlabel('Competitor Brand')
    plt.ylabel('Aggressiveness Level')
    plt.xticks(rotation=45)
    plt.yticks([1, 2, 3], ['Low', 'Medium', 'High'])
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf.getvalue()