from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import os

app = FastAPI(title="Snackification Visual Insights - KPI 11")

CSV_FILE_PATH = "section_FCSV/KPI11.csv"  # Update path if needed

@app.get("/F/KPI11/visualize")
def visualize_snackification():
    # Check file existence
    if not os.path.exists(CSV_FILE_PATH):
        raise HTTPException(status_code=404, detail="CSV file not found")

    try:
        # Load & preprocess
        df = pd.read_csv(CSV_FILE_PATH)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

        df['Platform'] = df['Platform'].str.strip()
        df['Meal Replaced'] = df['Meal Replaced'].str.strip()
        df['Snack Type'] = df['Snack Type'].str.strip()
        df['Mention of Haldiram'] = df['Mention of Haldiram'].str.strip().str.lower()
        df['Mention of Haldiram'] = df['Mention of Haldiram'].map({'yes': True, 'no': False})

        # Set style
        sns.set(style="whitegrid")

        # --- Plot 1: Meal Replaced ---
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        sns.countplot(
            data=df,
            x='Meal Replaced',
            order=df['Meal Replaced'].value_counts().index,
            palette='viridis',
            ax=axs[0]
        )
        axs[0].set_title("Meal Replacements by Snacks")
        axs[0].set_xlabel("Meal Replaced")
        axs[0].set_ylabel("Count")
        axs[0].tick_params(axis='x', rotation=45)

        # --- Plot 2: Monthly Mentions ---
        monthly_mentions = df[df['Mention of Haldiram']].groupby(df['Date'].dt.to_period('M')).size()
        monthly_mentions.index = monthly_mentions.index.astype(str)

        axs[1].bar(monthly_mentions.index, monthly_mentions.values, color='orange')
        axs[1].set_title("Monthly Mentions of Haldiram in Snack Contexts")
        axs[1].set_xlabel("Month")
        axs[1].set_ylabel("Mentions")
        axs[1].tick_params(axis='x', rotation=45)

        # --- Plot 3: Health Angle ---
        sns.countplot(
            data=df,
            x='Health Angle',
            order=df['Health Angle'].dropna().value_counts().index,
            palette='Set2',
            ax=axs[2]
        )
        axs[2].set_title("Snackification Posts with Health Angle")
        axs[2].set_xlabel("Health Mentioned")
        axs[2].set_ylabel("Post Count")
        axs[2].tick_params(axis='x', rotation=45)

        plt.tight_layout()

        # Save plots as image
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)

        return StreamingResponse(img_buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
