from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd

router = APIRouter()

FILE_PATH = "C_Physical_CSV/KPI1.csv"  # Update path based on your project structure

@router.get("/rising-search-queries")
async def get_rising_queries():
    try:
        # ✅ Load tab-delimited CSV
        df = pd.read_csv(FILE_PATH, delimiter="\t", engine="python", on_bad_lines='skip')

        # ✅ Clean and inspect
        df.columns = df.columns.str.strip()
        if 'Percentage.1' not in df.columns or 'Top' not in df.columns:
            return JSONResponse(status_code=400, content={"error": "Required columns not found in CSV."})

        # ✅ Filter for 'Breakout' in rising percentage column
        df['Percentage.1'] = df['Percentage.1'].astype(str).str.strip().str.lower()
        breakout_df = df[df['Percentage.1'] == 'breakout']

        # ✅ Extract and clean top queries
        rising_queries = breakout_df['Top'].dropna().drop_duplicates().tolist()

        return {
            "🔥 Top Rising Related Search Queries": rising_queries
        }

    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {FILE_PATH}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal Server Error: {str(e)}"})
