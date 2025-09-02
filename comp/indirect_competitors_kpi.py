import pandas as pd

def get_indirect_competitor_kpi():
    # 1. Read the competitor CSV (make sure the path is correct)
    file_path = 'data/indirect competitors.csv'  # Update if needed
    df = pd.read_csv(file_path)

    # 2. Check the column names to ensure they match
    print("Column Names: ", df.columns)

    # 3. Check the first few rows of the dataset to verify it looks correct
    print(df.head())

    # 4. Define categories for indirect competitors
    indirect_categories = ['western snacks', 'specialized bakeries', 'RTE']

    # 5. Filter indirect competitors based on categories
    indirect_competitors = df[df['category'].isin(indirect_categories)]

    # 6. Get unique indirect competitors
    indirect_competitor_names = indirect_competitors['Brand'].unique()

    # 7. Print results
    print("\n=== Number of Key Indirect Competitors Identified ===")
    print(f"Total indirect competitors: {len(indirect_competitor_names)}\n")
    print("Indirect competitors:")
    for competitor in indirect_competitor_names:
        print(f" - {competitor}")
        
    return {
        "total_indirect_competitors": len(indirect_competitor_names),
        "indirect_competitors": sorted(indirect_competitor_names.tolist())
    }