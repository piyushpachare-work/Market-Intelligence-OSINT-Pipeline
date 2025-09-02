from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

app = FastAPI(title="Discretionary Spending Visualizer")

CSV_FILE_PATH = "section_FCSV/KPI20.csv"  # Replace with the correct full path if needed

@app.get("/F/kpi20/visualize")
def visualize_discretionary_spending():
    # Validate file exists
    if not os.path.exists(CSV_FILE_PATH):
        raise HTTPException(status_code=404, detail="CSV file not found")

    try:
        # Load and clean data
        df = pd.read_csv(CSV_FILE_PATH, encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()

        relevant_cols = [
            "Date", "Source Type", "Source Name", "Quote / Observation",
            "Theme Category", "Mention of Haldiram (Yes/No)",
            "Region (if known)", "Notes / Summary"
        ]
        df = df[relevant_cols]

        # Filter for themes
        themes_of_interest = ["Cutting Back", "Brand Switching", "Affordable Alternatives"]
        df_filtered = df[df["Theme Category"].isin(themes_of_interest)]

        # Summary for bar chart
        theme_summary = df_filtered["Theme Category"].value_counts()

        # Mentions of Haldiram for pie chart
        haldiram_mentions = df_filtered["Mention of Haldiram (Yes/No)"].value_counts()

        # ---- Plotting ----
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))

        # Bar chart: Theme Category counts
        axs[0].bar(theme_summary.index, theme_summary.values, color='skyblue', edgecolor='black')
        axs[0].set_title("Number of Observations by Theme Category")
        axs[0].set_xlabel("Theme")
        axs[0].set_ylabel("Number of Quotes")
        axs[0].grid(axis='y', linestyle='--', alpha=0.6)

        # Pie chart: Mentions of Haldiram
        axs[1].pie(
            haldiram_mentions.values,
            labels=haldiram_mentions.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=['lightcoral', 'lightgreen']
        )
        axs[1].set_title("Mentions of Haldiram")

        plt.tight_layout()

        # Return as image response
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close(fig)
        img_buffer.seek(0)

        return StreamingResponse(img_buffer, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
