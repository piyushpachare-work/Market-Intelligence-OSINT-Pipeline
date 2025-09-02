import pandas as pd

def get_influencer_summary():
    # Step 1: Load the CSV file
    file_path = "data/use of influencers.csv"
    df_influencers = pd.read_csv(file_path)

    # Step 2: Clean up column names (remove extra spaces)
    df_influencers.columns = df_influencers.columns.str.strip()

    # Step 3: Drop rows with missing 'Company' or 'Use' values
    df_influencers.dropna(subset=['Company', 'Use (Yes/No)', 'Name of Influencer'], inplace=True)

    # Step 4: Group influencers by company
    grouped_influencers = df_influencers.groupby(['Company', 'Use (Yes/No)'])['Name of Influencer'].apply(', '.join).reset_index()

    # Step 5: Set pandas options to display all rows and columns
    pd.set_option('display.max_rows', None)  # No limit on rows
    pd.set_option('display.max_columns', None)  # No limit on columns
    pd.set_option('display.width', None)  # No limit on line width
    pd.set_option('display.max_colwidth', None)  # No limit on column width

    # Step 6: Display the grouped data
    print(grouped_influencers)

    # Step 7: Save the summarized data to a new CSV
    output_file_path = "data\\Competitor_Use_of_Influencers_Summarized.csv"
    grouped_influencers.to_csv(output_file_path, index=False)

    print(f"Competitor use of influencers summarized and saved to: {output_file_path}")
    return grouped_influencers.to_dict(orient="records")