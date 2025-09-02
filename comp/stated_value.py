import pandas as pd

def get_stated_value_propositions():
    # Step 1: Load the CSV file
    file_path = "data/Competitor Stated Value Proposi.csv"
    df_value_propositions = pd.read_csv(file_path)

    # Step 2: Inspect the data and clean up the columns if needed
    df_value_propositions.columns = df_value_propositions.columns.str.strip()

    # Step 3: Display the dataframe to check for any missing values
    print(df_value_propositions)

    # Step 4: Clean any missing or invalid rows if necessary
    df_value_propositions.dropna(subset=['Brand', 'Tagline / Slogan', 'Core Value Proposition', 'Key Messaging Themes'], inplace=True)

    # Step 5: Display the cleaned-up data
    print(df_value_propositions)

    # Step 6: Save the summarized data to a new CSV if desired
    output_file_path = "data\\Competitor_Stated_Value_Propositions_Summarized.csv"
    df_value_propositions.to_csv(output_file_path, index=False)

    print(f"Competitor stated value propositions summarized and saved to: {output_file_path}")
    return df_value_propositions.to_dict(orient="records")