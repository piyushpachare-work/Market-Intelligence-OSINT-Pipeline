from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import io

app = FastAPI()

@app.get("/F/KPI13/influencer-summary")
def get_influencer_summary():
    try:
        file_path = "section_FCSV/KPI13.csv"
        df = pd.read_csv(file_path, encoding='ISO-8859-1')

        # Clean column names
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

        # Fill missing values and clean text
        df['followers/subscribers'] = df['followers/subscribers'].fillna('Unknown')
        df['estimated_influence'] = df['estimated_influence'].str.strip().str.title()

        # Create summaries
        tone_summary = df['tone_on_haldiram/indian_snacks'].value_counts()
        influence_summary = df.groupby('estimated_influence')['influencer/media'].count()

        # Create subplots
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle("Influencer Analysis Summary", fontsize=16)

        # Plot tone summary
        axs[0].bar(tone_summary.index, tone_summary.values, color='skyblue')
        axs[0].set_title("Tone on Haldiram/Indian Snacks")
        axs[0].set_ylabel("Count")
        axs[0].set_xticklabels(tone_summary.index, rotation=45, ha='right')

        # Plot influence summary
        axs[1].bar(influence_summary.index, influence_summary.values, color='salmon')
        axs[1].set_title("Estimated Influence Level")
        axs[1].set_ylabel("Count")
        axs[1].set_xticklabels(influence_summary.index, rotation=45, ha='right')

        plt.tight_layout()

        # Save to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        return {"error": str(e)}
