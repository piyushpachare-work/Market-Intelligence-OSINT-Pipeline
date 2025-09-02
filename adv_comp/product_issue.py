import pandas as pd
import matplotlib.pyplot as plt
import io

def analyze_product_issues():
    # Step 1: Load the CSV File
    file_path = "data/competitor product issue.csv"
    df = pd.read_csv(file_path)

    # Step 2: Clean and Preprocess Data
    df['Date Reported / Period'] = pd.to_datetime(df['Date Reported / Period'], errors='coerce')

    # Step 3: Group by Competitor and Type of Incident to Count Frequency
    incident_counts = df.groupby(['Competitor', 'Type of Incident / Complaint Pattern']).size().reset_index(name='Incident Frequency')

    # Step 4: Group by Competitor and Severity to Get Frequency by Severity Level
    severity_counts = df.groupby(['Competitor', 'Severity']).size().reset_index(name='Severity Frequency')

    # Step 5: Plot Timeline of Incidents Over Time
    incident_timeline = df.groupby(df['Date Reported / Period'].dt.to_period('M')).size()
    incident_timeline.index = incident_timeline.index.astype(str)

    plt.figure(figsize=(10,6))
    incident_timeline.plot(kind='line')
    plt.title('Competitor Product Quality Issues Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Incidents')
    plt.grid(True)
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)

    # Step 6: Identify High-Impact Industry-Wide Issues (High Severity)
    high_severity_issues = df[df['Severity'] == 'High']
    print("High Severity Incidents (Industry-Wide):")
    print(high_severity_issues)

    # Step 7: Display Results
    print("\nIncident Frequency by Competitor and Type:")
    print(incident_counts)

    print("\nIncident Frequency by Severity:")
    print(severity_counts)

    return {
        "incident_counts": incident_counts.to_dict(orient="records"),
        "severity_counts": severity_counts.to_dict(orient="records"),
        "incident_timeline": incident_timeline.reset_index().rename(columns={0: "Incident Count", "Date Reported / Period": "Date"}).to_dict(orient="records"),
        "high_severity_issues": high_severity_issues.to_dict(orient="records")
    }

def get_product_issue_chart():
    file_path = "data/competitor product issue.csv"
    df = pd.read_csv(file_path)
    df['Date Reported / Period'] = pd.to_datetime(df['Date Reported / Period'], errors='coerce')
    incident_timeline = df.groupby(df['Date Reported / Period'].dt.to_period('M')).size()
    incident_timeline.index = incident_timeline.index.astype(str)

    plt.figure(figsize=(10,6))
    incident_timeline.plot(kind='line')
    plt.title('Competitor Product Quality Issues Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Incidents')
    plt.grid(True)
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf