"""Latih model Logistic Regression (logit biner) dari data/ukt.csv -> model.pkl"""
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FITUR = ["StatusOrtu", "Penghasilan", "Status_Rumah", "JMotor", "Jmobil", "DayaLis"]
TARGET = "KIPK"


def train(csv_path="data/ukt.csv", out="model.pkl"):
    df = pd.read_csv(csv_path)
    X_tr, X_te, y_tr, y_te = train_test_split(
        df[FITUR], df[TARGET], test_size=0.2, random_state=42, stratify=df[TARGET])
    model = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000))
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    print(f"Akurasi: {accuracy_score(y_te, pred):.3f} | Recall KIPK: {recall_score(y_te, pred):.3f}")
    model.fit(df[FITUR], df[TARGET])  # latih ulang dengan seluruh data
    joblib.dump(model, out)
    return model


if __name__ == "__main__":
    train()
