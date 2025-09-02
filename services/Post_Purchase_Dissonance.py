# services/post_purchase_dissonance.py

import pandas as pd
from collections import Counter
import io
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

class PostPurchaseDissonance:
    def __init__(self, csv_path=Path("KPI_Data") / "Post_Purchase_Dessonance.csv"):
        self.csv_path = csv_path
        self.df = None

    def load_data(self):
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {self.csv_path}")
        self.df = pd.read_csv(self.csv_path)
        required_cols = ['Sentiment', 'Expectation Mismatch', 'Dissonance Reason']
        missing_cols = [col for col in required_cols if col not in self.df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in CSV: {missing_cols}")
        # Filter only negative comments with expectation mismatch as Yes
        self.df = self.df[(self.df['Sentiment'] == 'Negative') & (self.df['Expectation Mismatch'] == 'Yes')]

    def generate_dissonance_chart(self):
        if self.df is None:
            self.load_data()

        reason_counts = Counter(self.df['Dissonance Reason'])
        top_reasons = reason_counts.most_common(5)

        if not top_reasons:
            raise ValueError("No dissonance reasons found in data")

        reasons = [r[0] for r in top_reasons]
        counts = [r[1] for r in top_reasons]

        plt.figure(figsize=(8,8))
        wedges, texts, autotexts = plt.pie(
            counts,
            labels=reasons,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Pastel1.colors,
            textprops={'fontsize': 12}
        )
        plt.title('Top 5 Post-Purchase Dissonance Reasons\n(by % of Negative Comments)', fontsize=14)
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf

def get_post_purchase_dissonance_chart():
    try:
        dissonance = PostPurchaseDissonance()
        img_buf = dissonance.generate_dissonance_chart()
        return StreamingResponse(img_buf, media_type="image/png")
    except FileNotFoundError as fe:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(fe))
    except ValueError as ve:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
