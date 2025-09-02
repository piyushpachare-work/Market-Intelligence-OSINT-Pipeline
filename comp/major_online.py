import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

def generate_major_online_heatmap():
    # Step 1: Read the CSV data into a DataFrame
    file_path = "data/Competitor Presence Score on Ma.csv"  # Replace with your actual path
    df = pd.read_csv(file_path)

    # Step 2: Clean the data (if necessary, like fixing column names, handling missing values)
    # For example, renaming columns and ensuring no NaN values
    df.columns = df.columns.str.strip()  # Strip extra spaces in column names
    df.fillna(0, inplace=True)  # Fill missing values with 0 (if any)

    # Step 3: Create a competitor presence score table (already done in CSV)
    # We'll use the table as is, but ensure that numeric data is properly handled

    # Step 4: Generate the heatmap
    # Set the competitor names as the index and e-commerce platforms as columns
    presence_data = df.set_index("Brand").drop(columns=["Own Website"])

    # Plot the heatmap using seaborn
    plt.figure(figsize=(10, 8))  # Adjust figure size as needed
    sns.heatmap(presence_data, annot=True, cmap="YlGnBu", cbar=True, linewidths=0.5)

    # Add titles and labels
    plt.title("Competitor Presence Score on Major E-commerce Platforms")
    plt.xlabel("E-commerce Platforms")
    plt.ylabel("Competitors")

    # Show the plot
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf