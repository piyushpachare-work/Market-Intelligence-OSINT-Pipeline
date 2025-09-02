from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = FastAPI()
router = APIRouter()

@router.get("/occasion-mentions")
async def generate_occasion_chart():
    try:
        # Step 1: Hardcoded data (you can replace with CSV reading if needed)
        data = {
            'Occasion': ['Celebration', 'Travel', 'Tea time', 'Holi', 'Party',
                         'Wedding', 'Birthday', 'Rakhi', 'Diwali', 'Gifting'],
            'Frequency': [4, 5, 14, 20, 3, 5, 1, 4, 4, 5]
        }
        df = pd.DataFrame(data)

        # Step 2: Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(df['Occasion'], df['Frequency'], color='orange')
        plt.title('Occasion Mentions Associated with Haldiram Products', fontsize=13)
        plt.xlabel('Occasion')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Step 3: Return image as PNG
        img_stream = BytesIO()
        plt.savefig(img_stream, format='png')
        plt.close()
        img_stream.seek(0)

        return StreamingResponse(img_stream, media_type="image/png")

    except Exception as e:
        return {"error": f"❌ Internal error: {str(e)}"}
