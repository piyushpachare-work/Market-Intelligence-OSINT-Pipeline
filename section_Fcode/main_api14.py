from fastapi import FastAPI, Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

app = FastAPI()

CSV_FILE = "section_FCSV/KPI14.csv"

def load_data():
    df = pd.read_csv(CSV_FILE, skipinitialspace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Sentiment Score'] = pd.to_numeric(df['Sentiment Score'], errors='coerce')
    df.dropna(subset=['Date', 'Sentiment Score'], inplace=True)
    return df

@app.get("/F/kpi14/ regulation")
def regulation_chart():
    df = load_data()
    sentiment_by_reg = df.groupby('Regulation/Event Title')['Sentiment Score'].mean().sort_values(ascending=False).head(20)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=sentiment_by_reg.values, y=sentiment_by_reg.index, palette="viridis")
    plt.title("Top 20 Regulation/Event Sentiment")
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")
