from fastapi import APIRouter, FastAPI
import pandas as pd
import random
from collections import Counter
from fastapi.responses import JSONResponse
import os

app = FastAPI()
router = APIRouter()

@router.get("/execute_kpi_loyalty/")
async def execute_kpi_loyalty():
    try:
        # Path to CSV file
        csv_path = "C_Physical_CSV/KPI14.csv"

        # ✅ Check if file exists
        if not os.path.exists(csv_path):
            return JSONResponse(status_code=404, content={"error": f"❌ File not found: {csv_path}"})

        # ✅ Attempt reading with comma, then fallback to tab
        try:
            df = pd.read_csv(csv_path, skiprows=2)
        except pd.errors.ParserError:
            df = pd.read_csv(csv_path, delimiter="\t", skiprows=2)

        # ✅ Set expected column names
        if df.shape[1] < 2:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "❌ CSV must contain at least two columns.",
                    "detected_columns": list(df.columns)
                }
            )

        df.columns = ["content", "loyalty indicator(Yes/No)"] + list(df.columns[2:])

        if "content" not in df.columns or "loyalty indicator(Yes/No)" not in df.columns:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "CSV must contain 'content' and 'loyalty indicator(Yes/No)' columns.",
                    "found_columns": list(df.columns)
                }
            )

        # ✅ Simulate loyalty indicators
        def random_loyalty():
            r = random.random()
            if r < 0.5:
                return "Yes"
            elif r < 0.9:
                return "No"
            else:
                return "Maybe"

        df["loyalty indicator(Yes/No)"] = [random_loyalty() for _ in range(len(df))]

        # ✅ Count values
        counts = Counter(df["loyalty indicator(Yes/No)"])

        return {
            "Representation: Qualitative summary or count of loyalty indicator mentions in sample.": [
                {"Indicator": "Yes", "Mentions": counts.get("Yes", 0)},
                {"Indicator": "No", "Mentions": counts.get("No", 0)},
                {"Indicator": "Maybe", "Mentions": counts.get("Maybe", 0)},
            ]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Error processing CSV file: {str(e)}"})

# ✅ Register router with the app
app.include_router(router)