import pandas as pd
import numpy as np

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()  # Standardize column names
    return df

def preprocess_data(df):
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Preserve Station ID & Name
    id_cols = ["station id", "station name"]
    drop_cols = ["longitude (degrees)", "latitude (degrees)", "elevation (m)", "code", "abbreviation"]

    # Keep only necessary columns
    df = df[[col for col in df.columns if col not in drop_cols]]

    # Define expected months & filter existing ones
    all_months = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
    existing_months = [col for col in all_months if col in df.columns]

    if not existing_months:
        raise ValueError("No valid month columns found in input data!")

    print("Before melting:", df.columns.tolist())  # ✅ Debugging step

    # Melt dataframe into long format
    df = df.melt(id_vars=["station id", "station name", "year"], 
             value_vars=["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"], 
             var_name="month", value_name="rainfall_amount")

    print("After melting:", df.head())  # ✅ Debugging step

    # Convert rainfall values to numeric
    df["rainfall_amount"] = pd.to_numeric(df["rainfall_amount"], errors="coerce")

    # Fill missing values with the mean
    df["rainfall_amount"] = df["rainfall_amount"].fillna(df["rainfall_amount"].mean())

    # Convert categorical 'month' to numeric
    df["month"] = df["month"].astype("category").cat.codes

    # Features and target
    X = df[id_cols + ["year", "month"]]
    y = df["rainfall_amount"]

    return X, y, id_cols
