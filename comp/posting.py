import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_posting_plot():
    # Load the file
    file_path = "data/Competitor Social Media Posting.csv"
    df = pd.read_csv(file_path)

    # Debug: check exact column names
    print("Columns in CSV:", df.columns.tolist())

    # Clean column names
    df.columns = df.columns.str.strip()
    df['Brand'] = df['Brand'].str.strip()

    # Ensure column exists with correct name after stripping
    df['Number of Posts'] = pd.to_numeric(df['Number of Posts'], errors='coerce')

    # Sort and plot
    df = df.sort_values(by='Number of Posts', ascending=False)

    plt.figure(figsize=(10, 6))
    bars = plt.barh(df['Brand'], df['Number of Posts'], color='mediumseagreen')

    # Annotate bars with values
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.2, bar.get_y() + bar.get_height() / 2,
                 str(int(width)), va='center', fontsize=9)

    plt.xlabel('Number of Posts (Last 30 Days)', fontsize=12)
    plt.title('Instagram Posting Frequency of Competitors', fontsize=14)
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf