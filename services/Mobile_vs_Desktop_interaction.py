# services/kpi_mobile_desktop.py

import pandas as pd
import matplotlib.pyplot as plt
import io
from pathlib import Path
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

def generate_mobile_desktop_bar_chart():
    try:
        csv_path = Path("KPI_Data") / "Mobile_vs_Desktop_Interaction.csv"

        # Check if CSV exists
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        df = pd.read_csv(csv_path)

        # Extract "Page Load Speed" row
        match = df[df['KPI'] == "Page Load Speed (KPI 59)"]
        if match.empty:
            raise ValueError("Row with KPI 'Page Load Speed (KPI 59)' not found.")

        pload = match.iloc[0]
        mobile_score_text = pload['Mobile Interaction']
        desktop_score_text = pload['Desktop Interaction']

        # Parse score
        mobile_score = int(mobile_score_text.split(':')[1].strip().split('/')[0])
        desktop_score = int(desktop_score_text.split(':')[1].strip().split('/')[0])

        # Plotting
        labels = ['Page Load Speed']
        x = range(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(6,4))
        ax.bar(x, [mobile_score], width, label='Mobile')
        ax.bar([i + width for i in x], [desktop_score], width, label='Desktop')

        ax.set_ylabel('Score (out of 100)')
        ax.set_title('Mobile vs Desktop Page Load Speed')
        ax.set_xticks([i + width/2 for i in x])
        ax.set_xticklabels(labels)
        ax.legend()
        plt.tight_layout()

        # Save to buffer and return
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")

    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
