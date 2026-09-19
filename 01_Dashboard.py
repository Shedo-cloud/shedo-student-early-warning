import streamlit as st
import pandas as pd

from utils import load_data, load_model, prepare_predictions


# ============================================================
# PAGE TITLE
# ============================================================

st.title("📊 Academic Dashboard")


# ============================================================
# UPLOAD STUDENT CSV
# ============================================================

st.subheader("📂 Student Data")

uploaded_file = st.file_uploader(
    "Upload student CSV file",
    type=["csv"]
)


# ============================================================
# LOAD STUDENT DATA
# ============================================================

if uploaded_file is not None:

    try:
        data = pd.read_csv(uploaded_file)

        st.success(
            f"Successfully uploaded {len(data)} student records."
        )

    except Exception as e:

        st.error(
            f"Unable to read the CSV file: {e}"
        )

        st.stop()

else:

    # Use previously uploaded data if available
    if "student_data" in st.session_state:

        data = st.session_state["student_data"]

    else:

        # Otherwise use the default CSV
        data = load_data()


# ============================================================
# CHECK DATA
# ============================================================

if data.empty:

    st.error(
        "No student data is available. "
        "Please upload a CSV file."
    )

    st.stop()


# ============================================================
# LOAD MODEL
# ============================================================

model = load_model()


if model is None:

    st.error(
        "Trained model was not found."
    )

    st.stop()


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Student_ID",
    "Attendance_Rate",
    "Missing_Assignments",
    "GPA_Trend",
    "Current_GPA",
    "Previous_GPA",
    "Assessment_Average",
    "Study_Activity"
]


missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]


if missing_columns:

    st.error(
        "The following required columns are missing:"
    )

    st.write(missing_columns)

    st.stop()


# ============================================================
# GENERATE RISK PREDICTIONS
# ============================================================

data = prepare_predictions(
    data,
    model
)


# Save processed data for the other pages
st.session_state["student_data"] = data


# ============================================================
# SUMMARY
# ============================================================

total = len(data)

high = len(
    data[data["Risk_Level"] == "High"]
)

moderate = len(
    data[data["Risk_Level"] == "Moderate"]
)

low = len(
    data[data["Risk_Level"] == "Low"]
)


# ============================================================
# SUMMARY CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Total Students",
    total
)


c2.metric(
    "High Risk",
    high
)


c3.metric(
    "Moderate Risk",
    moderate
)


c4.metric(
    "Low Risk",
    low
)


st.divider()


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader(
    "Student Risk Distribution"
)


risk_chart = pd.DataFrame({

    "Risk Level": [
        "Low",
        "Moderate",
        "High"
    ],

    "Students": [
        low,
        moderate,
        high
    ]

})


st.bar_chart(
    risk_chart.set_index(
        "Risk Level"
    )
)


# ============================================================
# RISK PROBABILITY
# ============================================================

st.subheader(
    "Risk Probability Distribution"
)


hist = pd.cut(

    data["Risk_Probability"],

    bins=[
        0,
        20,
        40,
        60,
        80,
        100
    ],

    labels=[
        "0–20%",
        "21–40%",
        "41–60%",
        "61–80%",
        "81–100%"
    ],

    include_lowest=True

)


distribution = (
    hist
    .value_counts()
    .sort_index()
)


st.bar_chart(
    distribution
)


# ============================================================
# STUDENTS REQUIRING ATTENTION
# ============================================================

st.subheader(
    "⚠️ Students Requiring Attention"
)


attention = data[
    data["Risk_Level"].isin(
        ["Moderate", "High"]
    )
].sort_values(
    "Risk_Probability",
    ascending=False
)


if attention.empty:

    st.success(
        "No students are currently classified as Moderate or High Risk."
    )

else:

    st.dataframe(

        attention[
            [
                "Student_ID",
                "Current_GPA",
                "GPA_Trend",
                "Attendance_Rate",
                "Missing_Assignments",
                "Risk_Probability",
                "Risk_Level"
            ]
        ],

        use_container_width=True
    )


# ============================================================
# VIEW ALL STUDENT DATA
# ============================================================

with st.expander(
    "🔎 View Student Data"
):

    st.dataframe(
        data,
        use_container_width=True
    )
