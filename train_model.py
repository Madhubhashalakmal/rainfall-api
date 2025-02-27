import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from data_preprocessing import load_data, preprocess_data

def train_model(file_path):
    df = load_data(file_path)
    X, y, _ = preprocess_data(df)

    # ✅ Drop non-numeric columns
    X = X.drop(columns=["station id", "station name"])  

    model = LinearRegression()
    model.fit(X, y)  # Train model

    # Save trained model
    joblib.dump(model, "rainfall_model.pkl")
    print("Model trained and saved successfully!")

if __name__ == "__main__":
    train_model("Data Sheet Rain forecast.csv")
