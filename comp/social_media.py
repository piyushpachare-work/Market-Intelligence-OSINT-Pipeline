import pandas as pd

def get_social_media_presence():
    # Step 1: Read the CSV data into a DataFrame
    file_path = "data/Competitor Social Media Platfor.csv"  # Replace with your actual path
    df = pd.read_csv(file_path)

    # Step 2: Clean the data (if necessary, like fixing column names, handling missing values)
    df.columns = df.columns.str.strip()  # Strip extra spaces in column names

    # Step 3: Generate a checklist-style table (Yes/No presence across social media platforms)
    # Here, the data is already in the correct format (Yes/No for each platform)
    # You can easily display it as a table

    print("Competitor Social Media Platform Presence:")
    print(df)

    # Optional: If you want to save the table as a new CSV file
    # df.to_csv("Competitor_Social_Media_Presence_Output.csv", index=False)

    return df.to_dict(orient="records")