import pandas as pd

def get_top_organic_keywords():
    # Load the CSV file
    df = pd.read_csv('sectionCdata/keyword_visibility.csv')

    # Define a custom order for Estimated Monthly Search Volume to sort correctly
    volume_order = {'High': 3, 'Medium': 2, 'Low': 1}

    # Map the order for sorting
    df['Volume_Score'] = df['Estimated Monthly Search Volume'].map(volume_order)

    # Sort by volume score descending then by relevance and keyword
    df_sorted = df.sort_values(by=['Volume_Score', 'Relevance', 'Keyword'], ascending=[False, True, True])

    # Select top 10 keywords and return only the 'Keyword' column as a list
    top_keywords = df_sorted.head(10)['Keyword'].tolist()
    return top_keywords