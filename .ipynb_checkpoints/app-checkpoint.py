from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load all predictions into memory for quick access
years = [2024, 2025, 2026, 2027]
predictions_by_year = {}

for year in years:
    file_name = f"predictions_{year}.csv"
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        predictions_by_year[year] = df
        print(f"✅ Loaded {file_name}")
    else:
        print(f"⚠️ Warning: {file_name} not found. Skipping {year}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Rainfall Prediction API is running!"})

@app.route("/predict", methods=["GET"])
def get_predictions():
    """
    API Endpoint: /predict
    Query Params:
      - station_id (int)  ✅ Required
      - year (int)        ✅ Required (2024-2027)
      - month (str)       ✅ Optional (jan, feb, etc.)
    Returns:
      - JSON with predicted rainfall
    """
    try:
        # Get request parameters
        station_id = request.args.get("station_id", type=int)
        year = request.args.get("year", type=int)
        month = request.args.get("month", default=None, type=str)

        # Validate inputs
        if not station_id or not year:
            return jsonify({"error": "Missing 'station_id' or 'year'"}), 400
        if year not in predictions_by_year:
            return jsonify({"error": "Year out of range (2024-2027)"}), 400

        # Filter data by station ID and year
        df = predictions_by_year[year]
        filtered_df = df[df["Station_ID"] == station_id]

        # Filter by month if provided
        if month:
            filtered_df = filtered_df[filtered_df["Month"].str.lower() == month.lower()]
        
        # Check if results exist
        if filtered_df.empty:
            return jsonify({"error": "No data found for given parameters"}), 404

        # Convert results to JSON
        results = filtered_df.to_dict(orient="records")
        return jsonify({"predictions": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
