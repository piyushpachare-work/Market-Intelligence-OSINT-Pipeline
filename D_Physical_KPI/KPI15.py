from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import os

app = FastAPI()
router = APIRouter()
app.include_router(router)

@router.get("/execute_kpi_gifting/")
async def execute_kpi_gifting():
    try:
        csv_path = "C_Physical_CSV/KPI15.csv"

        # ✅ Check if file exists
        if not os.path.isfile(csv_path):
            return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {csv_path}"})

        # ✅ Try reading with tab separator first (most common problem)
        try:
            df = pd.read_csv(csv_path, sep='\t', on_bad_lines='skip', engine='python')
            if df.shape[1] < 4:
                # Try comma separator fallback
                df = pd.read_csv(csv_path, sep=',', on_bad_lines='skip', engine='python')
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"❌ Failed to read CSV: {str(e)}"})

        # ✅ Require at least 4 columns
        if df.shape[1] < 4:
            return JSONResponse(
                status_code=400,
                content={
                    "error": f"❌ File must have at least 4 columns, found only {df.shape[1]}.",
                    "columns_found": list(df.columns)
                }
            )

        # ✅ Take first 4 columns
        df_cleaned = df.iloc[:, :4]
        df_cleaned.columns = [
            'description',
            'analysis/findings',
            'specific example/observations',
            'source'
        ]

        # ✅ Drop fully empty rows
        df_cleaned.dropna(how='all', inplace=True)

        summary = []
        for _, row in df_cleaned.iterrows():
            summary.append({
                "📝 Description": str(row['description']),
                "🔍 Findings": str(row['analysis/findings']),
                "💬 Observation": str(row['specific example/observations']),
                "📡 Source": str(row['source'])
            })

        return {
            "message": "✅ KPI 15 file processed successfully.",
            "total_records": len(summary),
            "summary": summary
        }

    except Exception as e:
        # Print to logs/console for debugging during development
        print(f"❌ Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"❌ Internal Server Error: {str(e)}"}
        )