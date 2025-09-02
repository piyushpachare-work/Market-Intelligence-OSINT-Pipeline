from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()
router = APIRouter()

# File path
FILE_PATH = "C_Physical_CSV/KPI7.csv"

@router.get("/comparison-points")
async def get_comparison_points():
    try:
        # Try loading with tab delimiter first, and fallback to comma
        try:
            df = pd.read_csv(FILE_PATH, delimiter='\t', engine='python', on_bad_lines='skip')
            if df.shape[1] < 2:
                df = pd.read_csv(FILE_PATH, delimiter=',', engine='python', on_bad_lines='skip')
        except Exception:
            df = pd.read_csv(FILE_PATH, delimiter=',', engine='python', on_bad_lines='skip')

        # Ensure expected columns
        if df.shape[1] < 3:
            return {"error": "❌ Expected at least 3 columns: Sample Text, Brand, Comparison Type."}

        # Get first 3 columns automatically
        sample_col, brand_col, type_col = df.columns[:3]

        # Clean and convert to string
        df[sample_col] = df[sample_col].astype(str)
        df[brand_col] = df[brand_col].astype(str)
        df[type_col] = df[type_col].astype(str)

        # Format output
        result_list = [
            {
                "Sample Text": row[sample_col],
                "Comparison Brand": row[brand_col],
                "Comparison Type": row[type_col]
            }
            for _, row in df.iterrows()
        ]

        return {
            "List of frequently mentioned comparison points": result_list
        }

    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {FILE_PATH}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal Server Error: {str(e)}"})

# Register router
app.include_router(router, prefix="/KPI7")
