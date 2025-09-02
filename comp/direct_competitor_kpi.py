import pandas as pd

def get_direct_competitor_kpi():
    # 1. Read the competitor CSV
    file_path = 'data/direct competitors.csv'
    df = pd.read_csv(file_path)

    # 2. Clean column names and drop rows with missing values
    df.columns = df.columns.str.strip()
    df = df[['Brand', 'category']].dropna()
    df['category'] = df['category'].str.strip().str.title()  # Normalize casing

    # 3. Define core categories
    categories = ['Namkeen', 'Sweets', 'Rte']
    competitor_dict = {}

    for category in categories:
        # Get unique brand names per category
        brands = sorted(df[df['category'] == category]['Brand'].unique())
        competitor_dict[category] = brands

    # 4. Print KPI
    print("=== Number of Key Direct Competitors Identified ===")
    total_unique_brands = set()

    for category, brands in competitor_dict.items():
        total_unique_brands.update(brands)
        print(f"\n{category} competitors ({len(brands)}):")
        for b in brands:
            print(f" - {b}")

    print(f"\nTotal unique direct competitors across all categories: {len(total_unique_brands)}")

    return {
        "competitors_by_category": competitor_dict,
        "total_unique_direct_competitors": len(total_unique_brands)
    }