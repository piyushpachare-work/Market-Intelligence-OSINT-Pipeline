import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def load_and_process_data(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=2)
        df.columns = [
            "Platform", "Product_Name", "Brand", "Weight_g", "Price_INR",
            "Discount_Percent", "Availability", "Delivery_Time", "Product_Link"
        ]

        df["Availability"] = df["Availability"].str.strip().str.lower()

        def rate_availability(val):
            if val == "in stock":
                return "High"
            elif val == "out of stock":
                return "Low"
            else:
                return "Medium"

        df["Qualitative_Rating"] = df["Availability"].apply(rate_availability)

        return df

    except Exception as e:
        print(f"Error processing file: {e}")
        return None


def generate_bar_chart_base64(df):
    try:
        grouped = df.groupby(["Platform", "Qualitative_Rating"]).size().unstack(fill_value=0)

        # Plotting
        grouped.plot(kind='barh', stacked=True, figsize=(10, 6), color=["#2ecc71", "#f1c40f", "#e74c3c"])
        plt.title("Platform-wise Product Availability (Qualitative Rating)")
        plt.xlabel("Number of Products")
        plt.ylabel("Platform")
        plt.legend(title="Rating")
        plt.tight_layout()

        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")

    except Exception as e:
        print(f"Error generating bar chart: {e}")
        return None


def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-8.csv")
    df = load_and_process_data(file_path)

    if df is not None and not df.empty:
        chart_base64 = generate_bar_chart_base64(df)
        high_count = df[df["Qualitative_Rating"] == "High"].shape[0]
        medium_count = df[df["Qualitative_Rating"] == "Medium"].shape[0]
        low_count = df[df["Qualitative_Rating"] == "Low"].shape[0]

        return {
            "kpi_name": "Platform-wise Availability Ratings",
            "records_count": len(df),
            "rating_counts": {
                "High": high_count,
                "Medium": medium_count,
                "Low": low_count
            },
            "chart_base64": chart_base64
        }
    else:
        return {
            "kpi_name": "Platform-wise Availability Ratings",
            "error": "Failed to load or process data"
        }