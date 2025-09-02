import pandas as pd
import matplotlib.pyplot as plt
import io
import textwrap
import matplotlib
matplotlib.use('Agg')
from fastapi.responses import StreamingResponse

CSV_FILE_PATH = "KPI_Data/Influence_Attribution.csv"

def generate_mentions_by_platform_image():
    df = pd.read_csv(CSV_FILE_PATH)

    if 'Mentioned Platform' not in df.columns or 'Influence Source Type' not in df.columns:
        raise ValueError("Required columns 'Mentioned Platform' or 'Influence Source Type' not found in CSV")

    grouped = df.groupby('Mentioned Platform')['Influence Source Type'].apply(list).to_dict()

    wrapped_mentions = {}
    total_lines = 0
    wrap_width = 30
    for platform, mentions in grouped.items():
        wrapped_text_lines = []
        for mention in mentions:
            wrapped_lines = textwrap.wrap(mention, width=wrap_width)
            wrapped_text_lines.extend(wrapped_lines)
        wrapped_mentions[platform] = wrapped_text_lines
        total_lines += len(wrapped_text_lines) + 1

    total_lines = max(1, total_lines)
    fig_height = max(8, total_lines * 0.3)

    fig, ax = plt.subplots(figsize=(14, fig_height))
    ax.axis('off')

    y = 1.0
    line_height = 1 / total_lines

    for platform, mentions_lines in wrapped_mentions.items():
        ax.text(0.05, y, platform, fontsize=12, fontweight='bold', va='top', ha='left')
        mentions_text = "\n".join(mentions_lines)
        ax.text(0.5, y, mentions_text, fontsize=10, va='top', ha='left')
        y -= (len(mentions_lines) + 1) * line_height

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
