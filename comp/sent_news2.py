import pandas as pd
import matplotlib.pyplot as plt
import math
from io import BytesIO

def generate_sent_news2_plot():
    # Step 1: Read file
    file_path = "data/news n mentions + sentiment.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Clean column names

    # Step 2: Verify required columns
    if not {'Brand', 'Sentiment'}.issubset(df.columns):
        raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")

    # Step 3: Define colors
    sentiment_colors = {
        'Positive': '#4CAF50',
        'Neutral': '#FF9800',
        'Negative': '#F44336'
    }

    # Step 4: Group by brand
    brands = df['Brand'].unique()
    num_brands = len(brands)

    # Step 5: Layout for subplots (3 columns)
    cols = 3
    rows = math.ceil(num_brands / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))

    # Flatten axes for easy iteration
    axes = axes.flatten() if num_brands > 1 else [axes]

    for i, brand in enumerate(brands):
        brand_df = df[df['Brand'] == brand]
        sentiment_counts = brand_df['Sentiment'].value_counts()

        axes[i].pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=[sentiment_colors.get(s, '#999999') for s in sentiment_counts.index],
            startangle=140
        )
        axes[i].set_title(f'{brand}')

    # Hide unused subplots if any
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.suptitle('Sentiment Breakdown by Brand', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf