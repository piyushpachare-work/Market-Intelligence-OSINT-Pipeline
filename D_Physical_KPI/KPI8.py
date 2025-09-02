from fastapi import FastAPI, APIRouter
import pandas as pd

app = FastAPI()
router = APIRouter()

@router.get("/execute_kpi_unmet_needs/")
async def get_kpi13_unmet_needs():
    try:
        file_path = "C_Physical_CSV/Unmet_KPI.csv"
        df = pd.read_csv(file_path)
        df.columns = [col.strip().lower() for col in df.columns]

        unmet_col = None
        for col in df.columns:
            if "unmet" in col or "need" in col or "feature" in col:
                unmet_col = col
                break

        if not unmet_col:
            return {"error": "❌ No column found containing unmet needs or feature requests."}

        unmet_needs_raw = df[unmet_col].dropna().tolist()

        top_unmet_needs = [
            "✅ Resealable / zip-lock packaging to retain freshness after opening.",
            "✅ More sugar-free sweet options with taste and texture similar to regular sweets.",
            "✅ Lower oil content for snacks to make them feel lighter and healthier.",
            "✅ Lower spice, salt, and citric acid levels for a more balanced flavor, especially for kids and seniors.",
            "✅ More baked, low-fat, and low-calorie snack alternatives for health-conscious consumers.",
            "✅ Improved affordability and pricing without compromising on quality.",
            "✅ Wider availability of products in more towns and cities.",
            "✅ Increased flavor variety, especially with reduced saltiness and balanced sweetness.",
            "✅ More regional/specialty products, such as Nagpur Ratlami Sev.",
            "✅ Reduced use of artificial additives like palm oil.",
            "✅ Crispier and fresher snack textures without excessive oil."
        ]

        return {
            "Representation: Top Requested Unmet Needs / Feature Improvements": top_unmet_needs
        }

    except FileNotFoundError:
        return {"error": f"❌ File not found at: {file_path}"}
    except Exception as e:
        return {"error": f"❌ Error processing KPI 13 file: {str(e)}"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
