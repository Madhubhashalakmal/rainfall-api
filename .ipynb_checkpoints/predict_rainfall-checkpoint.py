import joblib
import pandas as pd
from data_preprocessing import load_data, preprocess_data  

def predict_rainfall(file_path):
    # Load trained model
    model = joblib.load("rainfall_model.pkl")
    
    # Load and preprocess data
    df = load_data(file_path)
    X, _, id_cols = preprocess_data(df)  

    # Generate predictions for 2024, 2025, 2026, and 2027
    future_years = [2024, 2025, 2026, 2027]
    months = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
    
    predictions_dict = {year: [] for year in future_years}

    for year in future_years:
        for month_idx, month in enumerate(months):
            temp_X = X.copy()
            temp_X["year"] = year
            temp_X["month"] = month_idx  # Match category codes used in training
            temp_X = temp_X.drop(columns=["station id", "station name"])  # Remove non-numeric columns

            # Make predictions
            predicted_rainfall = model.predict(temp_X)

            # Store results
            for i in range(len(predicted_rainfall)):
                predictions_dict[year].append([
                    X.iloc[i]["station id"], 
                    X.iloc[i]["station name"], 
                    year, 
                    month, 
                    round(float(predicted_rainfall[i]), 4)  # ✅ Round to 4 decimal places
                ])

    # Save predictions to separate CSV files for each year
    for year in future_years:
        predicted_df = pd.DataFrame(predictions_dict[year], columns=["Station_ID", "Station_Name", "Year", "Month", "Predicted_Rainfall"])
        csv_filename = f"predictions_{year}.csv"
        predicted_df.to_csv(csv_filename, index=False)  # Save as CSV

    print("Predictions saved as CSV files: predictions_2024.csv, predictions_2025.csv, predictions_2026.csv, predictions_2027.csv!")

if __name__ == "__main__":
    predict_rainfall("Data Sheet Rain forecast.csv")
