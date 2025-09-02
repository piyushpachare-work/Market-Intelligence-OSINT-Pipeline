from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd
import os

router = APIRouter()

FILE_PATH = "C_Physical_CSV/KPI11.csv"  # Assuming it's a .tsv file with .csv extension

@router.get("/kpi11-sentiment-summary")
async def sentiment_summary():
    try:
        if not os.path.exists(FILE_PATH):
            return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {FILE_PATH}"})

        # Try reading with tab delimiter
        df = pd.read_csv(FILE_PATH, delimiter='\t')

        # Check if expected column exists
        expected_col = "Sentiment"
        if expected_col not in df.columns:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"❌ Column '{expected_col}' not found in CSV.",
                    "available_columns": list(df.columns)
                }
            )

        # Normalize values
        df[expected_col] = df[expected_col].astype(str).str.strip().str.capitalize()

        # Calculate sentiment distribution
        sentiment_distribution = df[expected_col].value_counts(normalize=True) * 100
        result = {sentiment: f"{pct:.2f}%" for sentiment, pct in sentiment_distribution.items()}

        return {
            "Representation: International Consumer Sentiment Distribution (%)": result
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal Server Error: {str(e)}"})