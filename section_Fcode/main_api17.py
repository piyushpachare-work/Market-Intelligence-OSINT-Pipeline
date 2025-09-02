from fastapi import FastAPI, Response
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io

app = FastAPI(title="KPI 17: Haldiram Food Tourism Visualization")

# -------- Relative CSV Path --------
CSV_FILENAME = "section_FCSV/KPI17.csv"  # Using raw string for Windows-style path

# -------- Check and Load Data --------
if not os.path.exists(CSV_FILENAME):
    raise FileNotFoundError(f"CSV file not found at: {CSV_FILENAME}")

df = pd.read_csv(CSV_FILENAME, encoding="ISO-8859-1")
df_clean = df.dropna(subset=['Association Strength'])

sns.set(style="whitegrid")

def generate_kpi17_figure():
    fig, axs = plt.subplots(1, 3, figsize=(20, 6))

    # Plot 1: Association Strength
    sns.countplot(data=df_clean, x='Association Strength',
                  order=['Weak', 'Moderate', 'Strong'],
                  palette='viridis', ax=axs[0])
    axs[0].set_title('Association Strength of Haldiram with Food Tourism')
    axs[0].set_xlabel('Association Strength')
    axs[0].set_ylabel('Number of Mentions')

    # Plot 2: Sentiment Pie Chart
    sentiment_counts = df_clean['Sentiment'].value_counts()
    axs[1].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
               startangle=140, colors=sns.color_palette('pastel'))
    axs[1].set_title('Sentiment Distribution of Haldiram Mentions')

    # Plot 3: Mentioned in Itinerary
    sns.countplot(data=df_clean, x='Mentioned in Context of Itinerary',
                  palette='magma', ax=axs[2])
    axs[2].set_title('Was Haldiram Mentioned in Travel Itineraries?')
    axs[2].set_xlabel('Mentioned in Itinerary')
    axs[2].set_ylabel('Number of Mentions')

    plt.tight_layout()
    return fig

def convert_plot_to_response(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return Response(content=buf.read(), media_type="image/png")

@app.get("/F/kpi17/visualize", summary="Visualize KPI 17 insights as a combined image")
def visualize_kpi17():
    fig = generate_kpi17_figure()
    return convert_plot_to_response(fig)
