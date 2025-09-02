import pandas as pd
import matplotlib.pyplot as plt
import io

def niche_targeting_plot():
    df = pd.read_csv("data/Competitor niche targeting effe.csv")
    clarity_map = {'High': 2, 'Medium': 1, 'Low': 0}
    resonance_map = {'High': 2, 'Medium': 1, 'Low': 0}
    df['Targeting Clarity Score'] = df['Targeting Clarity'].map(clarity_map)
    df['Resonance Level Score'] = df['Resonance Level'].map(resonance_map)

    bar_width = 0.35
    index = range(len(df))

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(index, df['Targeting Clarity Score'], bar_width, label='Targeting Clarity', alpha=0.7)
    ax.bar([i + bar_width for i in index], df['Resonance Level Score'], bar_width, label='Resonance Level', alpha=0.7)

    ax.set_xlabel('Competitor', fontsize=12)
    ax.set_ylabel('Effectiveness Score', fontsize=12)
    ax.set_title('Competitor Niche Targeting Effectiveness', fontsize=14)
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(df['Competitor'], rotation=45, ha='right')
    ax.legend()

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    return buf.getvalue()

if __name__ == "_main_":
    img_bytes = niche_targeting_plot()
    with open("niche_targeting_plot.png", "wb") as f:
        f.write(img_bytes)
    print("Plot saved as niche_targeting_plot.png")