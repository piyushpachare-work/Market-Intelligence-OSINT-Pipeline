from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()
router = APIRouter()

# ✅ Your CSV path
FILE_PATH = "C_Physical_CSV/KPI4.csv"

@router.get("/kpi4-psychographic-themes")
async def generate_kpi4_graph():
    try:
        # ✅ Read with tab delimiter
        df = pd.read_csv(FILE_PATH, skiprows=2, delimiter="\t", engine='python', on_bad_lines='skip')

        # ✅ Validate
        if df.shape[1] < 2:
            return {"error": "❌ CSV still doesn't have 2+ columns even after tab delimiter. Check file format manually."}

        df.columns = ["Psychographic Theme", "Frequency"]
        df.dropna(inplace=True)

        # ✅ Convert to int safely
        df["Frequency"] = pd.to_numeric(df["Frequency"], errors='coerce').fillna(0).astype(int)

        # ✅ Sort & Plot
        df_sorted = df.sort_values(by="Frequency", ascending=False)
        plt.figure(figsize=(10, 6))
        plt.barh(df_sorted["Psychographic Theme"], df_sorted["Frequency"], color='skyblue')
        plt.xlabel("Frequency")
        plt.title("Psychographic Themes in Haldiram Reviews & Social Posts")
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # ✅ Send as image
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)
        return StreamingResponse(img_bytes, media_type="image/png")

    except FileNotFoundError:
        return {"error": f"❌ File not found at: {FILE_PATH}"}
    except Exception as e:
        return {"error": f"❌ Internal error: {str(e)}"}

# ✅ Register the router
app.include_router(router, prefix="/KPI4")
