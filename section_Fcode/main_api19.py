import io
from fastapi import FastAPI, Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = FastAPI()

@app.get("/F/kpi19/chart")
def generate_chart():
    # Load CSV
    file_path = "section_FCSV/KPI19.csv"
    df = pd.read_csv(file_path, encoding='ISO-8859-1')

    # Clean Data
    df_cleaned = df[df['Challenge Type'].notnull()]
    df_cleaned['Challenge Type'] = df_cleaned['Challenge Type'].str.strip()
    challenge_counts = df_cleaned['Challenge Type'].value_counts()

    # Plot to PNG buffer
    plt.figure(figsize=(10, 6))
    sns.barplot(x=challenge_counts.values, y=challenge_counts.index, palette='coolwarm')
    plt.title('Top Cross-Cultural Adaptation Challenges in Export Markets')
    plt.xlabel('Number of Mentions')
    plt.ylabel('Challenge Type')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="image/png")
