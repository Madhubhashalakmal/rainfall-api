import pandas as pd

# Define future years
years = [2024, 2025, 2026, 2027]

# Placeholder for storing results
predictions_by_year = {}

# Read each CSV file and store in a dictionary
for year in years:
    file_name = f"predictions_{year}.csv"
    try:
        df = pd.read_csv(file_name)
        predictions_by_year[year] = df  # Store DataFrame in dictionary
        print(f"✅ Successfully loaded {file_name}")
    except FileNotFoundError:
        print(f"⚠️ Warning: {file_name} not found. Skipping this year.")

# Save all predictions to an Excel file with separate sheets
output_file = "predictions_by_year.xlsx"

with pd.ExcelWriter(output_file) as writer:
    for year, df in predictions_by_year.items():
        df.to_excel(writer, sheet_name=f"Predictions_{year}", index=False)

print(f"✅ Predictions saved in {output_file} with separate sheets for 2024, 2025, 2026 & 2027!")
