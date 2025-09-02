import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to convert follower/subscriber shorthand (e.g., "22.7K") to actual numbers
def convert_to_number(value):
    value = str(value).strip().lower()
    if value.endswith('k'):
        return float(value[:-1]) * 1_000
    elif value.endswith('m'):
        return float(value[:-1]) * 1_000_000
    elif value.replace(',', '').isdigit():
        return int(value.replace(',', ''))
    else:
        return 0  # default if value is unexpected or empty

# Function to generate the followers plot
def generate_followers_plot():
    # Step 1: Read CSV and clean column names
    file_path = "data/Social Media.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    # Step 2: Convert all follower columns to numeric values
    for col in df.columns[1:]:
        df[col] = df[col].apply(convert_to_number)

    # Step 3: Plot grouped bar chart
    platforms = df.columns[1:]  # exclude company name
    x = df['Company']
    bar_width = 0.2
    positions = range(len(x))

    # Set up the figure
    plt.figure(figsize=(14, 8))

    for i, platform in enumerate(platforms):
        plt.bar(
            [p + bar_width * i for p in positions],
            df[platform],
            width=bar_width,
            label=platform
        )

    # Formatting the chart
    plt.xlabel('Company')
    plt.ylabel('Follower Count')
    plt.title('Competitor Social Media Follower Count (Snapshot)')
    plt.xticks([p + bar_width for p in positions], x, rotation=45)
    plt.legend()
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf