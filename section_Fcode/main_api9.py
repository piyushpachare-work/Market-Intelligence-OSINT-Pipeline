from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import io
from collections import Counter

app = FastAPI()

def generate_all_region_charts(csv_filepath='section_FCSV/KPI9.csv'):


    try:
        df = pd.read_csv(csv_filepath, encoding='utf-8-sig')
    except Exception as e:
        return None, f"Failed to read file: {e}"

    df.columns = df.columns.map(lambda x: x.strip() if isinstance(x, str) else x)
    if df.columns[0].startswith('\ufeff'):
        df.rename(columns={df.columns[0]: df.columns[0].replace('\ufeff', '').strip()}, inplace=True)

    required_cols = ['User Context (Region - Implied/Stated)', 'Theme']
    if not all(col in df.columns for col in required_cols):
        return None, "Missing required columns"

    df.dropna(subset=required_cols, inplace=True)

    def normalize_region(context_str):
        context_lower = str(context_str).lower()
        if any(x in context_lower for x in ['north', 'delhi', 'lucknow', 'chandigarh', 'jaipur', 'punjabi']):
            return "North India"
        elif any(x in context_lower for x in ['south', 'bangalore', 'chennai', 'kerala', 'tamil nadu']):
            return "South India"
        elif any(x in context_lower for x in ['east', 'kolkata', 'bengal', 'assam', 'odisha']):
            return "East India"
        elif any(x in context_lower for x in ['west', 'mumbai', 'gujarat', 'pune']):
            return "West India"
        elif any(x in context_lower for x in ['central', 'bhopal', 'indore']):
            return "Central India"
        elif 'pan-india' in context_lower or 'anywhere' in context_lower:
            return "Pan-India"
        return "Other"

    df['Region_Normalized'] = df['User Context (Region - Implied/Stated)'].apply(normalize_region)

    unique_regions = df['Region_Normalized'].unique()
    n_regions = len(unique_regions)
    ncols = 2
    nrows = (n_regions + 1) // 2

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, nrows * 4))
    axs = axs.flatten()

    for i, region in enumerate(unique_regions):
        region_df = df[df['Region_Normalized'] == region]
        theme_counts = Counter(region_df['Theme'].str.title())
        if not theme_counts:
            axs[i].axis('off')
            continue
        themes, counts = zip(*theme_counts.most_common(5))
        axs[i].barh(list(reversed(themes)), list(reversed(counts)), color='skyblue')
        axs[i].set_title(region)
        axs[i].tick_params(axis='x', labelsize=8)
        axs[i].tick_params(axis='y', labelsize=8)

    for j in range(i + 1, len(axs)):
        axs[j].axis('off')

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    plt.close(fig)
    buffer.seek(0)

    return buffer, None

@app.get("/F/kpi9/plot")
def get_all_region_charts():
    buffer, error = generate_all_region_charts()
    if error:
        return {"error": error}
    return StreamingResponse(buffer, media_type="image/png")
