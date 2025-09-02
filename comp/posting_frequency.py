import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the CSV data into a DataFrame
file_path = "data/posting frequency.csv"  # Updated path to the correct file
df = pd.read_csv(file_path)

# Step 2: Check the column names to ensure there are no hidden spaces or typos
print("Columns in the CSV file:", df.columns)

# Clean the data by stripping any leading/trailing spaces in the column names
df.columns = df.columns.str.strip()

# Check again after cleaning
print("Cleaned columns:", df.columns)

# Step 3: Generate the bar chart for posting frequency
plt.figure(figsize=(12, 8))  # Adjust figure size as needed
plt.barh(df['Brand'], df['Posts in Last 30 Days'], color='skyblue')

# Add titles and labels
plt.title("Competitor Social Media Posting Frequency (Last 30 Days)")
plt.xlabel("Number of Posts")
plt.ylabel("Competitors")

# Display the plot
plt.tight_layout()
plt.show()