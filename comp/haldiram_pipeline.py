import os
import pandas as pd

# Step 1: Read Excel file with multiple sheets
def read_excel_file(file_path):
    try:
        # Load all sheets into a dictionary of DataFrames
        sheets = pd.read_excel(file_path, sheet_name=None)
        return sheets
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

# Step 2: Export each sheet to a separate CSV
def export_sheets_to_csv(sheets, output_directory):
    try:
        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        for sheet_name, data in sheets.items():
            # Save each sheet as a CSV file
            output_filename = os.path.join(output_directory, f"{sheet_name}.csv")
            data.to_csv(output_filename, index=False)
            print(f"Data from '{sheet_name}' exported to {output_filename}")
    except Exception as e:
        print(f"Error exporting sheets to CSV: {e}")

# Main pipeline function
def run_pipeline(excel_file_path, output_directory):
    # Step 1: Read the Excel file
    sheets = read_excel_file(excel_file_path)
    
    if sheets:
        # Step 2: Export each sheet as a CSV file
        export_sheets_to_csv(sheets, output_directory)

# Example usage
excel_file_path ="data/Competitor Litigation_Regulatory Action Frequency.xlsx"

output_directory = "data"  # Use raw string

run_pipeline(excel_file_path, output_directory)
