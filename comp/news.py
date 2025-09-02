import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_news_mentions_plot():
    # 1. Load the CSV
    file_path = "data/news.csv"
    df = pd.read_csv(file_path)

    # 2. Clean up column names
    df.columns = df.columns.str.strip()

    # 3. Check if 'Brand' is a valid column, else fix likely formatting issue
    if 'Brand' not in df.columns:
        # Try re-reading with manual header splitting if it’s a single combined column
        first_col = df.columns[0]
        if ',' in first_col:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
        else:
            raise ValueError(f"'Brand' column not found. Available columns: {df.columns.tolist()}")

    # 4. Count news mentions per brand
    news_counts = df['Brand'].value_counts().sort_values(ascending=False)

    # 5. Plot bar chart
    plt.figure(figsize=(12, 6))
    news_counts.plot(kind='bar', color='steelblue')
    plt.title("News Mentions per Brand")
    plt.xlabel("Brand")
    plt.ylabel("Number of Mentions")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf