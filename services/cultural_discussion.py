import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from io import BytesIO
from fastapi.responses import StreamingResponse

def generate_contextual_indicators_chart(filepath: str = "KPI_data/cultural_discussion.csv") -> StreamingResponse:
    # Load CSV and count indicators
    df = pd.read_csv(filepath)
    counter = Counter(df["Key Contextual Indicators"])
    
    # Sort and unpack
    indicators, counts = zip(*sorted(counter.items(), key=lambda x: x[1], reverse=True))
    
    # Plot bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(indicators, counts, color="skyblue")
    plt.xlabel("Key Contextual Indicators")
    plt.ylabel("Frequency")
    plt.title("Frequency of Key Contextual Indicators")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    # Save to bytes
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")
