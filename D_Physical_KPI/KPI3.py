from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()
router = APIRouter()

# ✅ File paths
INSTAGRAM_FILE = "C_Physical_CSV/Instagram.csv"
TWITTER_FILE = "C_Physical_CSV/Twitter.csv"

# ✅ Keyword listsfrom fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()
router = APIRouter()

# ✅ File paths
INSTAGRAM_FILE = "C_Physical_CSV/Instagram.csv"
TWITTER_FILE = "C_Physical_CSV/Twitter.csv"

# ✅ Keyword lists
indian_metros = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune']
festival_keywords = ['Diwali', 'Holi', 'Eid', 'Christmas', 'Navratri', 'Durga Puja', 'festival']
family_keywords = ['family', 'parents', 'mother', 'father', 'kids', 'children']

def keyword_presence(text_series, keywords):
    return text_series.dropna().apply(lambda x: any(keyword.lower() in x.lower() for keyword in keywords))

def combine_text_columns(df):
    return df.select_dtypes(include='object').apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

@router.get("/kpi12-social-patterns")
async def detect_instagram_twitter_patterns():
    try:
        # ✅ Load CSV with flexible parser
        insta_df = pd.read_csv(INSTAGRAM_FILE, engine='python', on_bad_lines='skip')
        twitter_df = pd.read_csv(TWITTER_FILE, engine='python', on_bad_lines='skip')

        # ✅ Combine all object/text columns into one per row
        insta_text = combine_text_columns(insta_df)
        twitter_text = combine_text_columns(twitter_df)

        # ✅ Analyze presence of keywords
        insta_metro_mentions = keyword_presence(insta_text, indian_metros)
        twitter_metro_mentions = keyword_presence(twitter_text, indian_metros)

        insta_festival_mentions = keyword_presence(insta_text, festival_keywords + family_keywords)
        twitter_festival_mentions = keyword_presence(twitter_text, festival_keywords + family_keywords)

        # ✅ Prepare response
        representation = []

        if insta_metro_mentions.mean() > 0.05 or twitter_metro_mentions.mean() > 0.05:
            representation.append("Mentions often come from users identifying with major Indian metros.")
        else:
            representation.append("No strong concentration of mentions from major Indian metros observed.")

        if insta_festival_mentions.mean() > 0.03 or twitter_festival_mentions.mean() > 0.03:
            representation.append("Some association with family or festival context observed.")
        else:
            representation.append("Minimal reference to family or festival-related contexts detected.")

        return {
            "Representation: Qualitative description of any observed patterns": representation
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"error": f"❌ File not found: {str(e)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal server error: {str(e)}"})

# ✅ Register router
app.include_router(router, prefix="/KPI12")

indian_metros = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune']
festival_keywords = ['Diwali', 'Holi', 'Eid', 'Christmas', 'Navratri', 'Durga Puja', 'festival']
family_keywords = ['family', 'parents', 'mother', 'father', 'kids', 'children']

def keyword_presence(text_series, keywords):
    return text_series.dropna().apply(lambda x: any(keyword.lower() in x.lower() for keyword in keywords))

def combine_text_columns(df):
    return df.select_dtypes(include='object').apply(lambda row: ' '.join(row.dropna()), axis=1)

@router.get("/kpi12-social-patterns")
async def detect_instagram_twitter_patterns():
    try:
        # Load data
        insta_df = pd.read_csv(INSTAGRAM_FILE)
        twitter_df = pd.read_csv(TWITTER_FILE)

        insta_text = combine_text_columns(insta_df)
        twitter_text = combine_text_columns(twitter_df)

        # Analyze
        insta_metro_mentions = keyword_presence(insta_text, indian_metros)
        twitter_metro_mentions = keyword_presence(twitter_text, indian_metros)

        insta_festival_mentions = keyword_presence(insta_text, festival_keywords + family_keywords)
        twitter_festival_mentions = keyword_presence(twitter_text, festival_keywords + family_keywords)

        # Build response
        representation = []

        if insta_metro_mentions.mean() > 0.05 or twitter_metro_mentions.mean() > 0.05:
            representation.append("Mentions often come from users identifying with major Indian metros.")
        else:
            representation.append("No strong concentration of mentions from major Indian metros observed.")

        if insta_festival_mentions.mean() > 0.03 or twitter_festival_mentions.mean() > 0.03:
            representation.append("Some association with family or festival context observed.")
        else:
            representation.append("Minimal reference to family or festival-related contexts detected.")

        return {
            "Representation: Qualitative description of any observed patterns": representation
        }

    except FileNotFoundError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Internal server error: {str(e)}"})
