from fastapi import APIRouter
from fastapi.responses import JSONResponse
import pandas as pd

router = APIRouter()

FILE_PATH = "C_Physical_CSV/KPI9.csv"

@router.get("/kpi9-observed-terms")
async def list_observed_terms():
    try:
        # Load the CSV with flexible delimiter and skip bad lines
        df = pd.read_csv(FILE_PATH, delimiter="\t", on_bad_lines='skip', engine='python')

        # Drop fully empty rows
        df.dropna(how="all", inplace=True)

        # Rename columns if file seems valid
        if df.shape[1] >= 3:
            df.columns = ["Term/Slang", "Meaning/Context", "Source Platform"] + [f"Extra_{i}" for i in range(3, len(df.columns))]
        else:
            return JSONResponse(status_code=400, content={"error": "❌ Not enough columns in CSV file."})

        # Build the output list
        output = []
        for _, row in df.iterrows():
            output.append({
                "Term/Slang": str(row["Term/Slang"]).strip(),
                "Meaning/Context": str(row["Meaning/Context"]).strip(),
                "Source Platform": str(row["Source Platform"]).strip()
            })

        return {
            "Representation: List of Observed Terms": output
        }

    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"error": f"❌ File not found at: {FILE_PATH}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal Error: {str(e)}"})
