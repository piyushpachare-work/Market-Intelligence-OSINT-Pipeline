import pandas as pd
import numpy as np

def get_pricing_tiers():
    # Load data from the specified file path
    data_file = "data/Competitor Pricing Tier Percept.csv"
    df = pd.read_csv(data_file)

    # Ensure 'Price per 100g (INR)' is numeric, handling any non-numeric values
    df['Price per 100g (INR)'] = pd.to_numeric(df['Price per 100g (INR)'], errors='coerce')

    # Try to get Haldiram's price per 100g, else use median as fallback
    haldiram_row = df[df['Brand'] == "Haldiram's"]
    if not haldiram_row.empty:
        ref_price = haldiram_row['Price per 100g (INR)'].iloc[0]
    else:
        ref_price = df['Price per 100g (INR)'].median()

    # Define a function to categorize pricing tier relative to reference price
    def categorize_pricing(row):
        price_per_100g = row['Price per 100g (INR)']
        if price_per_100g >= 1.5 * ref_price:
            return 'Premium'
        elif 0.75 * ref_price <= price_per_100g < 1.5 * ref_price:
            return 'Mid-Range'
        else:
            return 'Economy'

    # Apply the categorization function to all competitors
    df['Pricing Tier'] = df.apply(categorize_pricing, axis=1)

    # Create the final table to display competitor pricing tiers
    final_table = df[['Brand', 'Product', 'Size', 'Price (INR)', 'Price per 100g (INR)', 'E-commerce Platform', 'Pricing Tier']]

    # Replace non-finite values with None for JSON serialization
    final_table = final_table.replace([np.inf, -np.inf, np.nan], None)

    return final_table.to_dict(orient="records")