# services/trust_analysis.py

import pandas as pd
from collections import Counter
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_trust_analysis_plot(csv_file_path=Path("KPI_Data") / "Trust_Analysis.csv"):
    try:
        if not csv_file_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_file_path}")

        df = pd.read_csv(csv_file_path)

        if 'Trust-Related Keywords' not in df.columns:
            raise ValueError(f"'Trust-Related Keywords' column not found. Columns: {df.columns.tolist()}")

        all_keywords = []
        for keywords in df['Trust-Related Keywords'].dropna():
            kw_list = [kw.strip().lower() for kw in keywords.split(',')]
            all_keywords.extend(kw_list)

        if not all_keywords:
            raise ValueError("No trust-related keywords found in data")

        keyword_counts = Counter(all_keywords)
        keyword_df = pd.DataFrame(keyword_counts.items(), columns=['Keyword', 'Frequency'])
        keyword_df = keyword_df.sort_values(by='Frequency', ascending=False)

        plt.figure(figsize=(12, 6))
        plt.bar(keyword_df['Keyword'], keyword_df['Frequency'], color='teal')
        plt.title('Frequency of Trust-Related Keywords in Positive Reviews')
        plt.xlabel('Trust-Related Keywords')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)

        return StreamingResponse(img_buffer, media_type='image/png')

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
