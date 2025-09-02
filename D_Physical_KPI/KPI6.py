from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()
router = APIRouter()

# Path to your KPI 6 CSV file
FILE_PATH = "C_Physical_CSV/KPI6.csv"

@router.get("/platform-summary")
async def platform_usage_summary():
    try:
        # ✅ Read with tab delimiter and skip bad lines
        df = pd.read_csv(FILE_PATH, encoding='utf-8', delimiter='\t', engine='python', on_bad_lines='skip')

        # ✅ Check for enough columns
        if df.shape[1] < 1:
            return JSONResponse(status_code=400, content={"error": "❌ CSV file doesn't contain enough columns. Check delimiter."})

        # Convert all data to string
        df = df.astype(str)

        platforms = ['facebook', 'instagram', 'twitter']
        summary = {}

        for platform in platforms:
            filtered_df = df[df.apply(lambda row: row.str.lower().str.contains(platform).any(), axis=1)]

            summary[platform.capitalize()] = {
                "Mention Count": len(filtered_df),
                "Qualitative Insight": (
                    "High engagement with visuals and campaigns." if platform == "instagram" and len(filtered_df) > 0 else
                    "Quick comments, trending discussions." if platform == "twitter" and len(filtered_df) > 0 else
                    "Longer reviews and brand sharing in groups." if platform == "facebook" and len(filtered_df) > 0 else
                    "No mentions found."
                )
            }

        return {
            "Representation: Qualitative summary of platform usage for Haldiram discussions": summary
        }

    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {FILE_PATH}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal Server Error: {str(e)}"})

# ✅ Register router
app.include_router(router, prefix="/KPI6")
