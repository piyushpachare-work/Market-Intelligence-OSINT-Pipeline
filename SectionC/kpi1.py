import pandas as pd
import matplotlib.pyplot as plt
import io

def generate_search_volume_plot():
    df = pd.read_csv("sectionCdata/search_volume_trend.csv")
    df.set_index('Country', inplace=True)
    df_transposed = df.T
    df_transposed.index.name = 'Year'

    plt.figure(figsize=(12, 6))
    for country in df_transposed.columns:
        plt.plot(df_transposed.index, df_transposed[country], label=country, marker='o')
    plt.title("Haldiram Brand Search Volume Trend (Google Trends)", fontsize=14)
    plt.xlabel("Year")
    plt.ylabel("Search Interest")
    plt.legend(title="Country")
    plt.grid(True)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read()
