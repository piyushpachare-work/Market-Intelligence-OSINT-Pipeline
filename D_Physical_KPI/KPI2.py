from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()
router = APIRouter()

FILE_PATH = "C_Physical_CSV/KPI2.csv"

@router.get("/generate-graph")
async def generate_graph():
    try:
        # ✅ Step 1: Read CSV with TAB delimiter
        df = pd.read_csv(FILE_PATH, delimiter="\t", on_bad_lines='skip', engine="python")

        # ✅ Step 2: Clean column names (strip whitespace and quotes)
        df.columns = df.columns.str.strip().str.replace('"', '')

        # ✅ Step 3: Ensure required columns exist
        required_columns = ['Month', 'Buy Haldiram online', 'Haldiram near me', 'Haldiram price']
        if not all(col in df.columns for col in required_columns):
            return {
                "error": f"❌ Required columns missing. Found: {df.columns.tolist()}"
            }

        # ✅ Step 4: Drop invalid header rows
        df = df[df['Month'].notna() & (df['Month'].str.lower() != 'month')]

        # ✅ Step 5: Convert Month to datetime and set as index
        df['Month'] = pd.to_datetime(df['Month'], errors='coerce')
        df.dropna(subset=['Month'], inplace=True)
        df.set_index('Month', inplace=True)

        # ✅ Step 6: Convert other columns to numeric
        df[required_columns[1:]] = df[required_columns[1:]].apply(pd.to_numeric, errors='coerce')

        # ✅ Step 7: Plot the graph
        plt.figure(figsize=(14, 7))
        for column in required_columns[1:]:
            plt.plot(df.index, df[column], label=column)

        plt.title("Trends of Purchase-Intent Keywords Over Time", fontsize=16)
        plt.xlabel("Month", fontsize=12)
        plt.ylabel("Search Interest / Volume", fontsize=12)
        plt.legend(title="Keywords", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.tight_layout()

        # ✅ Step 8: Stream the plot image
        img_stream = BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close()
        img_stream.seek(0)

        return StreamingResponse(img_stream, media_type="image/png")

    except FileNotFoundError:
        return {"error": f"❌ File not found: {FILE_PATH}"}
    except Exception as e:
        return {"error": f"❌ Internal error: {str(e)}"}

# ✅ Register router
app.include_router(router, prefix="/KPI2")
