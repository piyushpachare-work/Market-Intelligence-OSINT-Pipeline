# services/basket_composition_chart.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from collections import Counter
from itertools import product
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
import matplotlib
matplotlib.use('Agg')  # For Docker/no-GUI environments

def get_basket_composition_chart():
    try:
        csv_path = Path("KPI_Data") / "Basket_Composition.csv"
        
        # Check if file exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)
        pair_counts = Counter()

        for _, row in df.iterrows():
            haldiram_items = [item.strip() for item in str(row['Haldiram Products Mentioned']).split(',')]
            other_items = [item.strip() for item in str(row['Other Items Bought Together']).split(',')]
            
            for pair in product(haldiram_items, other_items):
                pair_counts[tuple(sorted(pair))] += 1

        top_pairs = pair_counts.most_common(10)
        if not top_pairs:
            raise HTTPException(status_code=204, detail="No valid product pairs found.")

        pairs = [' & '.join(pair) for pair, _ in top_pairs]
        counts = [count for _, count in top_pairs]

        plt.figure(figsize=(10, 6))
        plt.barh(pairs[::-1], counts[::-1], color='teal')
        plt.xlabel("Number of Mentions")
        plt.title("Top 10 Frequently Co-mentioned Product Pairs")
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
