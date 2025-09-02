import pandas as pd
import matplotlib.pyplot as plt
import io

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-15.csv")
    df = pd.read_csv(file_path, skiprows=2)
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    df['Threat Level (High/Medium/Low)'] = df['Threat Level (High/Medium/Low)'].fillna('Unknown')

    threat_counts = df['Threat Level (High/Medium/Low)'].value_counts()

    # Generate bar chart
    plt.figure(figsize=(6, 4))
    threat_counts.plot(kind='bar', color='orange', edgecolor='black')
    plt.title("Private Label Threat Levels")
    plt.xlabel("Threat Level")
    plt.ylabel("Count")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return {
        "chart_buffer": buf,
        "kpi_name": "Private Label Threat Levels",
        "threat_summary": threat_counts.to_dict(),
        "total_records": len(df)
    }
import pandas as pd
import matplotlib.pyplot as plt
import io

def run_kpi(params):
    file_path = params.get("file_path", "Market_data/KPI-15.csv")
    df = pd.read_csv(file_path, skiprows=2)
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    df['Threat Level (High/Medium/Low)'] = df['Threat Level (High/Medium/Low)'].fillna('Unknown')

    threat_counts = df['Threat Level (High/Medium/Low)'].value_counts()

    # Generate bar chart
    plt.figure(figsize=(6, 4))
    threat_counts.plot(kind='bar', color='orange', edgecolor='black')
    plt.title("Private Label Threat Levels")
    plt.xlabel("Threat Level")
    plt.ylabel("Count")
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return {
        "chart_buffer": buf,
        "kpi_name": "Private Label Threat Levels",
        "threat_summary": threat_counts.to_dict(),
        "total_records": len(df)
    }