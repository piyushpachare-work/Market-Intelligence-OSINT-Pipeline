import pandas as pd
import matplotlib.pyplot as plt
import io
import re

# --- Utility Functions ---

def clean_col_name(col):
    """Cleans column names: lowercase, alphanumeric only (for matching)."""
    return re.sub(r'[^a-zA-Z0-9]', '', col).lower()

def extract_years(time_period_str):
    """Extracts start and end years from a string like '2023–2028' or '2023-2028'."""
    if not isinstance(time_period_str, str):
        return None
    time_period_str = time_period_str.replace('–', '-')  # normalize dash
    parts = time_period_str.split('-')
    if len(parts) != 2:
        return None
    try:
        start_year = int(parts[0].strip())
        end_year = int(parts[1].strip())
        return start_year, end_year
    except:
        return None

def find_column(df, target_name):
    """Find a column in df that matches the cleaned target name."""
    target_clean = clean_col_name(target_name)
    for col in df.columns:
        if clean_col_name(col) == target_clean:
            return col
    return None

# --- Main KPI Functionality ---

def run_kpi(params):
    """Processes KPI-2 CSV and returns average CAGR by midpoint year."""
    file_path = params.get("file_path", "Market_data/KPI-2.csv")
    df = pd.read_csv(file_path, skiprows=5)  # <-- skip metadata rows
    df.columns = df.columns.str.strip()

    # Locate columns
    cagr_col = find_column(df, "CAGR (%)")
    time_col = find_column(df, "Time Period")

    if cagr_col is None:
        return {"error": f"'CAGR (%)' column is missing. Found columns: {list(df.columns)}"}
    if time_col is None:
        return {"error": f"'Time Period' column is missing. Found columns: {list(df.columns)}"}

    # Filter and clean CAGR column
    df = df[df[cagr_col].notna()]
    df = df[df[cagr_col]
            .astype(str)
            .str.replace('%', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
            .str.match(r'^\d+(\.\d+)?$')]

    if df.empty:
        return {"error": "No valid numeric CAGR data found."}

    df[cagr_col] = df[cagr_col].astype(str).str.replace('%', '', regex=False).astype(float)

    # Extract years
    years = df[time_col].apply(extract_years)
    df = df[years.notnull()]
    if df.empty:
        return {"error": "No valid 'Time Period' data found."}

    df['Start Year'], df['End Year'] = zip(*years[years.notnull()])
    df['Mid Year'] = (df['Start Year'] + df['End Year']) / 2

    # Group by Mid Year
    cagr_trends = df.groupby('Mid Year')[cagr_col].mean().sort_index()
    result = [{"Mid Year": int(year), "Average CAGR (%)": round(value, 2)} for year, value in cagr_trends.items()]
    return {"data": result}

# --- Plot Functionality ---

def generate_plot_image(file_path: str):
    """Generates a plot of average CAGR over midpoint year and returns PNG image buffer."""
    df = pd.read_csv(file_path, skiprows=5)  # <-- skip metadata rows
    df.columns = df.columns.str.strip()

    # Locate columns
    cagr_col = find_column(df, "CAGR (%)")
    time_col = find_column(df, "Time Period")

    if cagr_col is None:
        raise ValueError(f"'CAGR (%)' column is missing in the dataset. Found: {list(df.columns)}")
    if time_col is None:
        raise ValueError(f"'Time Period' column is missing in the dataset. Found: {list(df.columns)}")

    # Filter and clean CAGR column
    df = df[df[cagr_col].notna()]
    df = df[df[cagr_col]
            .astype(str)
            .str.replace('%', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
            .str.match(r'^\d+(\.\d+)?$')]

    if df.empty:
        raise ValueError("No valid numeric CAGR data found.")

    df[cagr_col] = df[cagr_col].astype(str).str.replace('%', '', regex=False).astype(float)

    # Extract years
    years = df[time_col].apply(extract_years)
    df = df[years.notnull()]
    if df.empty:
        raise ValueError("No valid 'Time Period' data found.")

    df['Start Year'], df['End Year'] = zip(*years[years.notnull()])
    df['Mid Year'] = (df['Start Year'] + df['End Year']) / 2

    # Group by Mid Year
    cagr_trends = df.groupby('Mid Year')[cagr_col].mean().sort_index()
    if cagr_trends.empty:
        raise ValueError("No valid data to plot after grouping.")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(cagr_trends.index, cagr_trends.values, marker='o', linestyle='-', color='royalblue')
    plt.title("Average CAGR (%) Trend by Mid Year")
    plt.xlabel("Mid Year")
    plt.ylabel("Average CAGR (%)")
    plt.grid(True)
    plt.tight_layout()

    # Save as image buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf