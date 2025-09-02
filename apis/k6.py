import pandas as pd
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def load_and_process_k6(file_path: str):
    """
    Load the CSV data, detect technology mentions, and prepare summary dataframe.
    """
    df = pd.read_csv(file_path)

    technology_keywords = [
        'AI', 'Artificial Intelligence', 'Machine Learning', 'Blockchain', 'IoT',
        'Smart Packaging', 'Sustainable Packaging', 'Automation', 'Robotics',
        'Data Analytics', 'Cloud Computing', 'Digital Twin', 'Sensor Technology'
    ]

    tech_descriptions = {
        'AI': 'Used for demand forecasting, quality control, and process optimization.',
        'Artificial Intelligence': 'Used for automation and intelligent decision-making in supply chains.',
        'Machine Learning': 'Helps predict spoilage, consumer preferences, and optimize logistics.',
        'Blockchain': 'Improves traceability and transparency in the food supply chain.',
        'IoT': 'Enables real-time monitoring of storage, temperature, and logistics.',
        'Smart Packaging': 'Improves shelf life and provides freshness indicators.',
        'Sustainable Packaging': 'Reduces environmental impact and supports circular economy.',
        'Automation': 'Enhances food processing efficiency and reduces human error.',
        'Robotics': 'Used in harvesting, packaging, and processing to increase speed and safety.',
        'Data Analytics': 'Helps in making informed decisions using production and sales data.',
        'Cloud Computing': 'Enables centralized access to data and real-time processing.',
        'Digital Twin': 'Simulates supply chain processes for better optimization.',
        'Sensor Technology': 'Monitors environmental conditions like humidity and temperature.'
    }

    text_data = df.astype(str).apply(lambda row: ' '.join(row), axis=1)

    tech_mentions = defaultdict(list)
    for row_text in text_data:
        for tech in technology_keywords:
            if re.search(rf'\b{re.escape(tech)}\b', row_text, re.IGNORECASE):
                context = row_text[:300] + "..." if len(row_text) > 300 else row_text
                tech_mentions[tech].append(context)

    summary = []
    for tech in technology_keywords:
        mentions = len(tech_mentions.get(tech, []))
        if mentions > 0:
            summary.append({
                "Technology": tech,
                "Mentions": mentions,
                "Relevance Description": tech_descriptions.get(tech, "N/A"),
                "Example Context": tech_mentions[tech][0] if tech_mentions[tech] else "N/A"
            })

    result_df = pd.DataFrame(summary).sort_values(by="Mentions", ascending=False)
    return result_df


def generate_bar_chart_base64(df: pd.DataFrame):
    """
    Generate a horizontal bar chart and return it as a base64-encoded PNG string.
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Mentions", y="Technology", data=df, palette="crest")
    plt.title("Technology Mentions in Food Sector Data")
    plt.xlabel("Number of Mentions")
    plt.ylabel("Technology")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return img_base64


def generate_plot_image(file_path: str):
    """
    Generate bar chart image and return it as BytesIO (for direct image response).
    """
    df = load_and_process_k6(file_path)
    if df.empty:
        raise ValueError("No technology mentions found to generate chart.")

    plt.figure(figsize=(12, 6))
    sns.barplot(x="Mentions", y="Technology", data=df, palette="crest")
    plt.title("Technology Mentions in Food Sector Data")
    plt.xlabel("Number of Mentions")
    plt.ylabel("Technology")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer


def run_kpi(params: dict):
    """
    Main function to be called by FastAPI route.
    Accepts params dict, expects 'file_path' key optionally.
    Returns JSON-serializable dict.
    """
    file_path = params.get("file_path", "Market_data/KPI-6.csv")

    try:
        df = load_and_process_k6(file_path)
        if df.empty:
            return {"error": "No technology mentions found in the data."}

        chart_base64 = generate_bar_chart_base64(df)

        return {
            "kpi_name": "Technology Mentions in Food Sector",
            "total_technologies_detected": len(df),
            "summary_table": df[["Technology", "Mentions", "Relevance Description"]].to_dict(orient="records"),
            "chart_base64_png": chart_base64
        }
    except Exception as e:
        return {"error": f"Failed to process KPI-6 data: {str(e)}"}
