import pandas as pd

def get_weaknesses_summary():
    # Step 1: Load the CSV file
    file_path = "data/Competitor Perceived Weaknesses.csv"
    df_weaknesses = pd.read_csv(file_path)

    # Step 2: Clean the column names
    df_weaknesses.columns = df_weaknesses.columns.str.strip()

    # Step 3: Split the 'brand' and 'perceived weakness' based on the colon ":".
    df_weaknesses['Brand'] = df_weaknesses['brand'].str.split(':').str[0].str.strip()
    df_weaknesses['Perceived Weaknesses'] = df_weaknesses['percieved weakness']

    # Step 4: Drop the original columns if needed
    df_weaknesses = df_weaknesses[['Brand', 'Perceived Weaknesses']]

    # Step 5: Remove any extra rows if needed and make sure the data is clean
    df_weaknesses.dropna(subset=['Brand', 'Perceived Weaknesses'], inplace=True)

    # Step 6: Grouping weaknesses by Brand (to combine multiple weaknesses into one row per brand)
    weaknesses_summary = df_weaknesses.groupby('Brand').agg({
        'Perceived Weaknesses': lambda x: '\n- '.join(x)
    }).reset_index()

    # Step 7: Display the results
    print(weaknesses_summary)

    # Step 8: Save the summarized data to a new CSV
    output_file_path = "data/Competitor_Perceived_Weaknesses_Summarized.csv"
    weaknesses_summary.to_csv(output_file_path, index=False)

    print(f"Competitor perceived weaknesses summarized and saved to: {output_file_path}")
    
    return weaknesses_summary.to_dict(orient="records")