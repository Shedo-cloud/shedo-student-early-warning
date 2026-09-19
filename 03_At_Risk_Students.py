import streamlit as st

from utils import (
    load_data,
    load_model,
    prepare_predictions,
    identify_risk_factors
)


st.title("⚠️ Students Requiring Academic Support")


data = load_data()
model = load_model()

data = prepare_predictions(
    data,
    model
)


high = data[
    data["Risk_Level"] == "High"
].sort_values(
    "Risk_Probability",
    ascending=False
)


moderate = data[
    data["Risk_Level"] == "Moderate"
].sort_values(
    "Risk_Probability",
    ascending=False
)


tab1, tab2 = st.tabs([
    "🔴 High Risk",
    "🟡 Moderate Risk"
])


with tab1:

    st.write(
        f"{len(high)} students currently fall "
        "into the high-risk category."
    )

    st.dataframe(
        high[
            [
                "Student_ID",
                "Current_GPA",
                "GPA_Trend",
                "Attendance_Rate",
                "Missing_Assignments",
                "Assessment_Average",
                "Risk_Probability"
            ]
        ],
        use_container_width=True
    )


with tab2:

    st.write(
        f"{len(moderate)} students currently fall "
        "into the moderate-risk category."
    )

    st.dataframe(
        moderate[
            [
                "Student_ID",
                "Current_GPA",
                "GPA_Trend",
                "Attendance_Rate",
                "Missing_Assignments",
                "Assessment_Average",
                "Risk_Probability"
            ]
        ],
        use_container_width=True
    )
