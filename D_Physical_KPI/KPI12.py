from fastapi import APIRouter, FastAPI
import pandas as pd
from textblob import TextBlob
from fastapi.responses import JSONResponse
import os

app = FastAPI()
router = APIRouter()

def get_sentiment(text: str) -> str:
    if not isinstance(text, str) or text.strip() == "":
        return "Neutral"
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

@router.get("/execute_kpi12/")
async def analyze_kpi12_sentiment():
    try:
        csv_path = "C_Physical_CSV/KPI12.csv"

        # ✅ Check if file exists
        if not os.path.exists(csv_path):
            return JSONResponse(status_code=404, content={"error": f"❌ File not found: {csv_path}"})

        # ✅ Try reading CSV with comma, then fallback to tab
        try:
            df = pd.read_csv(csv_path)
        except pd.errors.ParserError:
            df = pd.read_csv(csv_path, delimiter="\t")

        # ✅ Ensure at least one content column
        if df.shape[1] < 1:
            return JSONResponse(
                status_code=400,
                content={"error": "❌ The CSV file must contain at least one content column."}
            )

        # ✅ Rename for clarity
        df.columns = ['content'] + [f'col_{i}' for i in range(1, len(df.columns))]

        # ✅ Sentiment Analysis
        df['Computed Sentiment'] = df['content'].astype(str).apply(get_sentiment)

        # ✅ Filter Positive and Negative
        filtered_df = df[df['Computed Sentiment'].isin(['Positive', 'Negative'])]

        total = len(filtered_df)
        positive_count = (filtered_df['Computed Sentiment'] == 'Positive').sum()
        negative_count = (filtered_df['Computed Sentiment'] == 'Negative').sum()

        if total == 0:
            return {"message": "No Positive or Negative sentiments found in content."}

        positive_percent = round((positive_count / total) * 100, 2)
        negative_percent = round((negative_count / total) * 100, 2)

        return {
            "Representation: Summary of positive and negative sentiment percentages.": {
                "Positive": f"{positive_percent}%",
                "Negative": f"{negative_percent}%"
            }
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"❌ Error processing KPI 12 file: {str(e)}"}
        )

# ✅ Register the router
app.include_router(router)