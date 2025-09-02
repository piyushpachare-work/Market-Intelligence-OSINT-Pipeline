import pandas as pd

# Read CSV
file_path = "data/Partnership Network Mapping.csv"
df = pd.read_csv(file_path)

# Clean columns
df.columns = [col.strip() for col in df.columns]

# Drop empty rows (if any)
df.dropna(subset=["Competitor", "Partnership Type", "Partner(s)"], inplace=True)

# Display in readable format
#print("\nCompetitor Partnership Network Mapping:\n")
#for _, row in df.iterrows():
#    competitor = row['Competitor']
#    p_type = row['Partnership Type']
#    partner = row['Partner(s)']
#    details = row['Details']
#    
#    print(f"{competitor} - [{p_type}] with '{partner}': {details}")

# (Optional) Save cleaned output
#output_path = "data/Competitor_Partnership_Network_Clean.csv"
#df.to_csv(output_path, index=False)
#print(f"\n Cleaned partnership data saved to: {output_path}")

# New function to be used by FastAPI endpoint:
def get_partnership_data():
    """
    Returns the cleaned partnership network data as list of dicts for API response.
    """
    return df.to_dict(orient='records')