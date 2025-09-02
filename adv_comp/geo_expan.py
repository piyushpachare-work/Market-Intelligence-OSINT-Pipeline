# plotting.py (adv_comp/geo_expan.py)

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

def geo_expansion_endpoint(csv_path: str = "data/Competitor Geographic Expansion.csv") -> bytes:
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df_clean = df[df['Date'].notna()]

    plt.figure(figsize=(12, 6))

    for i, row in df_clean.iterrows():
        plt.plot([row['Date'], row['Date']], [i, i+1], marker='o', markersize=5, label=row['Competitor'])
        plt.text(row['Date'], i + 0.5, f"{row['Competitor']}\n{row['Expansion Type']} - {row['Location']}",
                 fontsize=10, ha='left', va='bottom')

    plt.title("Competitor Geographic Expansion Timeline", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Competitor", fontsize=12)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gcf().autofmt_xdate()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()