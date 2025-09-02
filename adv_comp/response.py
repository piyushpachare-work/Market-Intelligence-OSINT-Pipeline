import pandas as pd

CSV_PATH = "data/Competitor Response to Haldiram.csv"

def load_competitor_responses():
    df = pd.read_csv(CSV_PATH)

    # Drop rows with missing values in required columns
    df.dropna(subset=["Haldiram Trigger", "Competitor", "Reaction / Activity", "Date (Reaction)"], inplace=True)

    full_responses = df.to_dict(orient="records")

    trigger_groups_df = df.groupby("Haldiram Trigger")["Competitor"].apply(list).reset_index()
    reactions_by_trigger = trigger_groups_df.to_dict(orient="records")

    high_confidence_df = df[df["Confidence Level"] == "High"]
    high_confidence_responses = high_confidence_df.to_dict(orient="records")

    return {
        "full_responses": full_responses,
        "reactions_by_trigger": reactions_by_trigger,
        "high_confidence_responses": high_confidence_responses,
    }