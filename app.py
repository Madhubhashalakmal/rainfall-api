from flask import Flask, jsonify, request
import pandas as pd
import joblib
from data_preprocessing import preprocess_data

app = Flask(__name__)

# Load trained model
model = joblib.load("rainfall_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be in JSON format"}), 415  # Unsupported Media Type

        data = request.get_json()
        df = pd.DataFrame(data)

        # Preprocess data
        X, _, _ = preprocess_data(df)

        # ✅ Drop non-numeric columns (must match training step)
        if "station id" in X.columns and "station name" in X.columns:
            id_cols = X[["station id", "station name"]]  # Keep ID columns for reference
            X = X.drop(columns=["station id", "station name"])
        else:
            return jsonify({"error": "Missing required columns: 'station id' and 'station name'"}), 400

        # Generate predictions for 2024, 2025, 2026, and 2027
        future_years = [2024, 2025, 2026, 2027]
        months = ["jan", "feb", "mar", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
        predictions_dict = {year: [] for year in future_years}

        for year in future_years:
            for month_idx, month in enumerate(months):
                temp_X = X.copy()
                temp_X["year"] = year
                temp_X["month"] = month_idx  # Match category codes used in training

                # Make predictions
                predicted_rainfall = model.predict(temp_X)

                # Store results
                for i in range(len(predicted_rainfall)):
                    predictions_dict[year].append({
                        "Station_ID": int(id_cols.iloc[i]["station id"]),
                        "Station_Name": id_cols.iloc[i]["station name"],
                        "Year": year,
                        "Month": month,
                        "Predicted_Rainfall": round(float(predicted_rainfall[i]), 4)
                    })

        return jsonify({"predictions": predictions_dict})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Bad Request

if __name__ == "__main__":
    app.run(debug=True)
