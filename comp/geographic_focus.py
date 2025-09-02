import pandas as pd

def get_geographic_focus():
    # Step 1: Read the CSV file
    file_path = "data/Geographic Focus.csv"  # ✅ Update this path if needed
    df = pd.read_csv(file_path)

    # Step 2: Print column names to verify correct reading
    print("=== Columns in CSV ===")
    print(df.columns)

    # Step 3: Rename columns for consistency (only if needed)
    df.rename(columns={
        'Competitor': 'Brand',
        'Geographic Focus': 'Focus',
        'Notes': 'Notes'
    }, inplace=True)

    # Step 4: Clean whitespace from text fields
    df['Brand'] = df['Brand'].astype(str).str.strip()
    df['Focus'] = df['Focus'].astype(str).str.strip()
    df['Notes'] = df['Notes'].astype(str).str.strip()

    # Step 5: Add a Region Category based on 'Focus' string
    def classify_region(focus):
        focus = focus.lower()
        if 'global' in focus or 'export' in focus:
            return 'Global'
        elif 'national' in focus:
            return 'National'
        else:
            return 'Regional'

    df['Region Category'] = df['Focus'].apply(classify_region)

    # Step 6: Sort the data by Brand name
    df_sorted = df.sort_values(by='Brand')

    # Step 7: Print the cleaned table
    print("\n=== Cleaned Competitor Geographic Focus Table ===")
    print(df_sorted[['Brand', 'Focus', 'Region Category']])

    # Step 8: Export to a cleaned CSV
    output_path = "data/cleaned_geographic_focus.csv"
    df_sorted.to_csv(output_path, index=False)
    print(f"\n Cleaned CSV saved to: {output_path}")
    
    return df_sorted[['Brand', 'Focus', 'Region Category']].to_dict(orient="records")