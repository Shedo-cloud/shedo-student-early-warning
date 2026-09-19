import streamlit as st

from utils import (
    load_data,
    load_model,
    prepare_predictions
)


st.title("📥 Reports & Downloads")


data = load_data()
model = load_model()

data = prepare_predictions(
    data,
    model
)


# ------------------------------------------------
# ALL RESULTS
# ------------------------------------------------

st.subheader(
    "Complete Student Risk Dataset"
)


all_columns = [
    "Student_ID",
    "Attendance_Rate",
    "Missing_Assignments",
    "GPA_Trend",
    "Current_GPA",
    "Previous_GPA",
    "Assessment_Average",
    "Study_Activity",
    "Risk_Probability",
    "Risk_Level"
]


all_csv = data[
    all_columns
].to_csv(
    index=False
)


st.download_button(
    "📥 Download All Student Results",
    data=all_csv,
    file_name="student_risk_results.csv",
    mime="text/csv"
)


# ------------------------------------------------
# HIGH RISK
# ------------------------------------------------

st.subheader(
    "High-Risk Students"
)


high = data[
    data["Risk_Level"] == "High"
]


high_csv = high[
    all_columns
].to_csv(
    index=False
)


st.download_button(
    "📥 Download High-Risk Students",
    data=high_csv,
    file_name="high_risk_students.csv",
    mime="text/csv"
)


# ------------------------------------------------
# MODERATE RISK
# ------------------------------------------------

st.subheader(
    "Moderate-Risk Students"
)


moderate = data[
    data["Risk_Level"] == "Moderate"
]


moderate_csv = moderate[
    all_columns
].to_csv(
    index=False
)


st.download_button(
    "📥 Download Moderate-Risk Students",
    data=moderate_csv,
    file_name="moderate_risk_students.csv",
    mime="text/csv"
)
