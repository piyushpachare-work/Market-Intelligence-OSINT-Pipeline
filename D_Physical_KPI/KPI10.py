from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
import os
import traceback

router = APIRouter()

@router.get("/execute_kpi15/")
async def execute_kpi15():
    file_path = r"C_Physical_CSV\KPI15.csv"  # Update path as per your folder structure
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return JSONResponse(status_code=404, content={"error": "CSV file not found at path."})

        # Read the file with correct separator (tab-separated)
        df = pd.read_csv(file_path, sep='\t', encoding='utf-8')

        # Debug info: check shape and head
        print(f"Dataframe shape: {df.shape}")
        print(df.head())

        # Ensure required columns exist
        expected_columns = [
            'No.',
            'Description',
            'Analysis/Findings',
            'Specific Examples/Observations',
            'Source'
        ]

        # Check if all expected columns exist
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            return JSONResponse(status_code=400, content={"error": f"Missing columns: {missing_cols}"})

        # Drop any unnecessary columns beyond expected
        df = df[expected_columns]

        # Fill NaNs with empty strings to avoid nulls in JSON
        df.fillna("", inplace=True)

        # Convert to list of dicts
        result = df.to_dict(orient="records")

        return {
            "Representation: Qualitative summary of gifting mentions observed.": result
        }

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Exception:\n{tb}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "details": str(e)})
