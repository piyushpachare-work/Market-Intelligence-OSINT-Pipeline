import pandas as pd

def get_strategic_pivot_dossier():
    """
    Returns the competitor strategic pivot dossier as list of dicts for API response.
    """
    # Read the original CSV
    file_path = "data/pivot.csv"
    df = pd.read_csv(file_path)

    # Clean column names if needed
    df.columns = [col.strip() for col in df.columns]

    # Build dossier entries
    dossiers = []
    for _, row in df.iterrows():
        competitor = row['Competitor']
        count = row['Number of Variants/Flavors Launched']
        period = row['Period']
        category = row['Product Category']
        details = row['Details of Variants/Flavors']
        
        description = f"Launched {count} new variants in {period} across {category}: {details.strip()}."
        
        dossiers.append({
            "Competitor": competitor,
            "Category of Strategic Pivot": "Product Diversification",
            "Description of Pivot": description
        })

    # Convert to DataFrame
    df_dossier = pd.DataFrame(dossiers)

    # Show output in console
    print("\n Competitor Strategic Pivot Dossier:\n")
    print(df_dossier.to_string(index=False))

    # Save to CSV
    output_path = "data/Competitor_Strategic_Pivot_Dossier.csv"
    df_dossier.to_csv(output_path, index=False)
    print(f"\n Strategic pivot dossiers saved to: {output_path}")

    return df_dossier.to_dict(orient="records")