# ============================================================
# STUDENT EARLY-WARNING SYSTEM
# MACHINE LEARNING BACKEND
# ============================================================

import os
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)


# ============================================================
# 1. SETTINGS
# ============================================================

RANDOM_STATE = 42
N_STUDENTS = 2000

MODEL_PATH = "models/student_risk_model.pkl"
DATA_PATH = "data/synthetic_student_data.csv"


# Create folders if they do not exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)


# ============================================================
# 2. GENERATE SYNTHETIC STUDENT DATA
# ============================================================

np.random.seed(RANDOM_STATE)

student_ids = [
    f"ST{str(i).zfill(4)}"
    for i in range(1, N_STUDENTS + 1)
]


# ------------------------------------------------------------
# Attendance
# ------------------------------------------------------------

attendance = np.random.uniform(
    50,
    100,
    N_STUDENTS
)


# ------------------------------------------------------------
# Missing assignments
# ------------------------------------------------------------

missing_assignments = np.random.poisson(
    lam=3,
    size=N_STUDENTS
)

missing_assignments = np.clip(
    missing_assignments,
    0,
    15
)


# ------------------------------------------------------------
# Previous GPA
# ------------------------------------------------------------

previous_gpa = np.random.uniform(
    1.5,
    4.0,
    N_STUDENTS
)


# ------------------------------------------------------------
# GPA trend
# ------------------------------------------------------------

gpa_trend = np.random.uniform(
    -1.5,
    1.5,
    N_STUDENTS
)


# ------------------------------------------------------------
# Current GPA
# ------------------------------------------------------------

current_gpa = previous_gpa + gpa_trend

current_gpa = np.clip(
    current_gpa,
    0.0,
    4.0
)


# ------------------------------------------------------------
# Assessment average
# ------------------------------------------------------------

assessment_average = np.random.uniform(
    35,
    100,
    N_STUDENTS
)


# ------------------------------------------------------------
# Study activity
# ------------------------------------------------------------

study_activity = np.random.uniform(
    10,
    100,
    N_STUDENTS
)


# ============================================================
# 3. CREATE DATAFRAME
# ============================================================

data = pd.DataFrame({

    "Student_ID": student_ids,

    "Attendance_Rate": attendance,

    "Missing_Assignments": missing_assignments,

    "GPA_Trend": gpa_trend,

    "Current_GPA": current_gpa,

    "Previous_GPA": previous_gpa,

    "Assessment_Average": assessment_average,

    "Study_Activity": study_activity

})


# ============================================================
# 4. CREATE SYNTHETIC TARGET
# ============================================================
#
# IMPORTANT:
#
# This target is artificially generated for development.
# It is NOT real academic outcome data.
#
# In the final system, At_Risk must come from real
# historical outcomes defined by the institution.
# ============================================================

risk_score = (

    (100 - attendance) * 0.30

    + missing_assignments * 2.5

    - gpa_trend * 4.0

    + (4.0 - current_gpa) * 5.0

    + (100 - assessment_average) * 0.15

    + (100 - study_activity) * 0.10

)


# Add random variation
risk_score += np.random.normal(
    0,
    3,
    N_STUDENTS
)


# Convert score into binary target
data["At_Risk"] = (
    risk_score > 25
).astype(int)


# ============================================================
# 5. SAVE SYNTHETIC DATA
# ============================================================

data.to_csv(
    DATA_PATH,
    index=False
)

print("\nSynthetic dataset created:")
print(DATA_PATH)

print("\nDataset shape:")
print(data.shape)


# ============================================================
# 6. DEFINE FEATURES
# ============================================================

features = [

    "Attendance_Rate",

    "Missing_Assignments",

    "GPA_Trend",

    "Current_GPA",

    "Previous_GPA",

    "Assessment_Average",

    "Study_Activity"

]


X = data[features]

y = data["At_Risk"]


# ============================================================
# 7. CHECK CLASS DISTRIBUTION
# ============================================================

print("\nClass distribution:")

print(
    y.value_counts()
)


print("\nClass proportions:")

print(
    y.value_counts(normalize=True)
)


# ============================================================
# 8. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=RANDOM_STATE,

    stratify=y

)


print("\nTraining samples:")
print(len(X_train))

print("\nTesting samples:")
print(len(X_test))


# ============================================================
# 9. CREATE RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(

    n_estimators=300,

    max_depth=8,

    min_samples_split=5,

    min_samples_leaf=2,

    class_weight="balanced",

    random_state=RANDOM_STATE

)


# ============================================================
# 10. TRAIN MODEL
# ============================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 11. MAKE TEST PREDICTIONS
# ============================================================

predictions = model.predict(
    X_test
)

probabilities = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# 12. EVALUATE MODEL
# ============================================================

accuracy = accuracy_score(
    y_test,
    predictions
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)


print("\n======================================")
print("MODEL PERFORMANCE")
print("======================================")

print(
    f"\nAccuracy: {accuracy:.4f}"
)

print(
    f"ROC-AUC: {roc_auc:.4f}"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# ============================================================
# 13. FEATURE IMPORTANCE
# ============================================================

importance = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})


importance = importance.sort_values(
    "Importance",
    ascending=False
)


print("\nFeature Importance:")

print(
    importance
)


# ============================================================
# 14. SAVE TRAINED MODEL
# ============================================================

joblib.dump(

    model,

    MODEL_PATH

)


print("\n======================================")

print(
    f"Model saved to: {MODEL_PATH}"
)

print("======================================")


# ============================================================
# 15. PREDICTION FUNCTION
# ============================================================

def predict_student(

    attendance_rate,

    missing_assignments,

    gpa_trend,

    current_gpa,

    previous_gpa,

    assessment_average,

    study_activity

):

    student = pd.DataFrame({

        "Attendance_Rate": [
            attendance_rate
        ],

        "Missing_Assignments": [
            missing_assignments
        ],

        "GPA_Trend": [
            gpa_trend
        ],

        "Current_GPA": [
            current_gpa
        ],

        "Previous_GPA": [
            previous_gpa
        ],

        "Assessment_Average": [
            assessment_average
        ],

        "Study_Activity": [
            study_activity
        ]

    })


    probability = model.predict_proba(
        student
    )[0][1]


    prediction = model.predict(
        student
    )[0]


    if prediction == 1:

        status = "Potentially Needs Support"

    else:

        status = "No Risk Flag"


    return {

        "Status": status,

        "Risk_Probability": probability,

        "Features": student.iloc[0].to_dict()

    }


# ============================================================
# 16. TEST LIVE PREDICTION
# ============================================================

example_prediction = predict_student(

    attendance_rate=75,

    missing_assignments=5,

    gpa_trend=-0.3,

    current_gpa=2.6,

    previous_gpa=2.9,

    assessment_average=60,

    study_activity=40

)


print("\n======================================")
print("EXAMPLE STUDENT PREDICTION")
print("======================================")

print(
    f"\nStatus: "
    f"{example_prediction['Status']}"
)

print(
    f"Risk probability: "
    f"{example_prediction['Risk_Probability']:.2%}"
)
