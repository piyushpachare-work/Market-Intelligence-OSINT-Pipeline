from fastapi import APIRouter
import pandas as pd

router = APIRouter()

@router.get("/profile-completeness")
def get_profile_completeness():
    # Step 1: Read the competitor data from CSV
    file_path = "data/Competitor Profile Completeness.csv"
    df = pd.read_csv(file_path)

    # Step 2: Scoring system (keeping High, Medium, Low, N/A as they are)
    scoring_map = {
        'High': 3,
        'Medium': 2,
        'Low': 1,
        'N/A': 0
    }

    # Apply the scoring to each relevant column
    df['Product Range Info Score'] = df['Product Range Info'].map(scoring_map)
    df['Distribution Info Score'] = df['Distribution Info'].map(scoring_map)
    df['Marketing Messaging Score'] = df['Marketing Messaging'].map(scoring_map)
    df['News Mentions Score'] = df['News Mentions'].map(scoring_map)

    # Step 3: Calculate the total score
    df['Total Score'] = df[['Product Range Info Score', 'Distribution Info Score', 
                             'Marketing Messaging Score', 'News Mentions Score']].sum(axis=1)

    # Step 4: Convert numerical scores back to High/Medium/Low
    def score_to_label(score):
        if score == 12:
            return 'High'
        elif score >= 7:
            return 'Medium'
        else:
            return 'Low'

    # Convert the total score to High/Medium/Low
    df['Total Score Label'] = df['Total Score'].apply(score_to_label)

    # Step 5: Clean the output (keep necessary columns)
    df_cleaned = df[['Competitor', 'Product Range Info', 'Distribution Info', 
                     'Marketing Messaging', 'News Mentions', 'Total Score Label']]

    # Step 6: Sort competitors based on the Total Score (by label)
    df_sorted = df_cleaned.sort_values(by='Total Score Label', ascending=False)

    # Step 7: Display the Competitor Profile Completeness table
    print("\n=== Competitor Profile Completeness ===")
    print(df_sorted)

    # Optionally: Export this table to a new CSV for reporting purposes
    output_file = 'data/competitor_profile_completeness.csv'
    df_sorted.to_csv(output_file, index=False)

    return df_sorted.to_dict(orient="records")