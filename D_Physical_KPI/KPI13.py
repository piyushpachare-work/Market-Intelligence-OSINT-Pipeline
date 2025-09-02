from fastapi import APIRouter, FastAPI
import pandas as pd
import os
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter()

@router.get("/execute_kpi13/")
async def execute_kpi13():
    try:
        csv_path = "C_Physical_CSV/KPI13.csv"

        # ✅ File existence check
        if not os.path.exists(csv_path):
            return JSONResponse(status_code=404, content={"error": f"❌ File not found: {csv_path}"})

        # ✅ Try reading with different delimiters
        try:
            df = pd.read_csv(csv_path)
        except pd.errors.ParserError:
            try:
                df = pd.read_csv(csv_path, delimiter="\t")
            except pd.errors.ParserError:
                df = pd.read_csv(csv_path, delimiter=";")

        # ✅ Drop empty rows
        df.dropna(how='all', inplace=True)

        # ✅ Assign expected column names (only if it matches expected number)
        expected_cols = [
            "sample content",
            "discovery channel category",
            "reason",
            "no.of mentions",
            "discovery types",
            "remarks"
        ]

        if len(df.columns) < len(expected_cols):
            return JSONResponse(
                status_code=400,
                content={"error": f"❌ Expected at least {len(expected_cols)} columns but found {len(df.columns)}"}
            )

        df.columns = expected_cols + list(df.columns[len(expected_cols):])

        # ✅ Clean 'no.of mentions' column
        df["no.of mentions"] = pd.to_numeric(df["no.of mentions"], errors="coerce").fillna(0).astype(int)

        # ✅ Group by discovery channel
        summary = df.groupby("discovery channel category").agg({
            "no.of mentions": "sum",
            "reason": lambda x: ', '.join(x.dropna().unique()),
            "discovery types": lambda x: ', '.join(x.dropna().unique()),
            "remarks": lambda x: ', '.join(x.dropna().unique())
        }).reset_index()

        output = []
        for _, row in summary.iterrows():
            output.append({
                "discovery_channel": row["discovery channel category"],
                "total_mentions": int(row["no.of mentions"]),
                "key_reasons": row["reason"],
                "discovery_types": row["discovery types"],
                "remarks": row["remarks"]
            })

        return {
            "message": "✅ KPI 13 discovery summary generated successfully.",
            "result": output
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Error processing KPI 13: {str(e)}"})

# ✅ Register the router
app.include_router(router)