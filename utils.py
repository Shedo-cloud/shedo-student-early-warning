import os
import joblib
import pandas as pd
import numpy as np


DATA_PATH = "synthetic_student_data.csv"
MODEL_PATH = "student_risk_model.pkl"

FEATURES = [
    "Attendance_Rate",
    "Missing_Assignments",
    "GPA_Trend",
    "Current_GPA",
    "Previous_GPA",
    "Assessment_Average",
    "Study_Activity",
]


def load_data():

    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()

    return pd.read_csv(DATA_PATH)


def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    return joblib.load(MODEL_PATH)


def prepare_predictions(data, model):

    result = data.copy()

    X = result[FEATURES]

    result["Predicted_At_Risk"] = model.predict(X)

    result["Risk_Probability"] = (
        model.predict_proba(X)[:, 1] * 100
    )

    result["Risk_Level"] = result["Risk_Probability"].apply(
        classify_risk
    )

    return result


def classify_risk(probability):

    if probability < 30:
        return "Low"

    elif probability < 60:
        return "Moderate"

    return "High"


def identify_risk_factors(student):

    factors = []

    if student["Attendance_Rate"] < 75:
        factors.append("Attendance")

    if student["Missing_Assignments"] >= 4:
        factors.append("Missing assignments")

    if student["GPA_Trend"] < 0:
        factors.append("Declining GPA")

    if student["Assessment_Average"] < 60:
        factors.append("Assessment performance")

    if student["Study_Activity"] < 40:
        factors.append("Low study activity")

    return factors
