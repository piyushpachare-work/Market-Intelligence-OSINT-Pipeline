from fastapi import FastAPI
from fastapi.responses import Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

app = FastAPI()

@app.get("/F/kpi15/visualize", response_class=Response, responses={200: {"content": {"image/png": {}}}})
def visualize():
    # Load and process data
    df = pd.read_csv("section_FCSV/KPI15.csv", encoding="ISO-8859-1")
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    
    # --- Plot 1: Google Trends and Social Mentions Over Time ---
    plt.figure(figsize=(14, 6))
    for category in df['Product Category'].unique():
        subset = df[df['Product Category'] == category]
        plt.plot(subset['Date'], subset['Google Trends'], label=f"{category} - GT", linestyle='-')
        plt.plot(subset['Date'], subset['Social Mentions'], label=f"{category} - SM", linestyle='--')
    plt.title('Google Trends and Social Mentions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.legend(loc='upper right', fontsize='small', ncol=3)
    plt.grid(True)
    plt.tight_layout()

    # Save the figure to memory
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png')
    plt.close()
    img_bytes.seek(0)

    # Return image as response
    return Response(content=img_bytes.read(), media_type="image/png")
