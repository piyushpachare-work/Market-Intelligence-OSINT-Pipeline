import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def generate_new_product_plot():
    # Step 1: Load the CSV file
    file_path = "data/Competitor New Product Launches.csv"
    df_product_launches = pd.read_csv(file_path)

    # Step 2: Clean up the data (remove extra spaces, ensure all data is in the correct format)
    df_product_launches.columns = df_product_launches.columns.str.strip()

    # Step 3: Display the dataframe to inspect the data
    print(df_product_launches)

    # Step 4: Create a simple bar chart to visualize the frequency of new product launches by competitor
    plt.figure(figsize=(10, 6))
    plt.bar(df_product_launches['Brand'], df_product_launches['Number of New Products'], color='skyblue')

    # Step 5: Customize the plot (titles, labels, etc.)
    plt.title('Number of New Product Launches by Competitor', fontsize=16)
    plt.xlabel('Brand', fontsize=12)
    plt.ylabel('Number of New Products', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = BytesIO()
    # Step 6: Save the plot to a file if required
    plt.savefig(buf, format="png", dpi=300)
    plt.close()
    buf.seek(0)
    return buf

# Note: The function generate_new_product_plot can now be called to execute the above steps and generate the plot.