import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_share_of_search_plot():
    df = pd.read_csv("sectionCdata/share_of_search.csv")
    df = df.drop(columns=['Share of Search %'])
    df.set_index('Brand', inplace=True)
    df_transposed = df.T
    df_transposed.index.name = 'Year'

    plt.figure(figsize=(12, 6))
    for brand in df_transposed.columns:
        plt.plot(df_transposed.index, df_transposed[brand], label=brand, marker='o')
    plt.title("Haldiram vs Competitors – Search Volume Trend (Google Trends)", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Search Interest")
    plt.legend(title="Brand")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()