import pandas as pd
import numpy as np

def load_talent_acquisition_data():
    file_path = "data/Competitor Talent Acquisition .csv"
    df = pd.read_csv(file_path)

    df.dropna(subset=["Competitor", "Recent Job Postings"], inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Fill missing values with a placeholder string
    df["Key Roles"] = df["Key Roles"].fillna("Not specified")
    df["Hiring Focus"] = df["Hiring Focus"].fillna("Not specified")
    df["Recent Job Postings"] = df["Recent Job Postings"].fillna("Not specified")

    # Prepare list of dictionaries for better readability in JSON
    summary_list = []
    for _, row in df.iterrows():
        summary_list.append({
            "Competitor": row["Competitor"],
            "Recent Job Postings": row["Recent Job Postings"],
            "Key Roles": row["Key Roles"],
            "Hiring Focus": row["Hiring Focus"],
        })

    return summary_list