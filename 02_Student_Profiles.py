import streamlit as st

from utils import (
    load_data,
    load_model,
    prepare_predictions,
    identify_risk_factors
)


st.title("👨‍🎓 Student Profiles")


data = load_data()
model = load_model()

if data.empty or model is None:
    st.error(
        "Student data or trained model is unavailable."
    )
    st.stop()


data = prepare_predictions(
    data,
    model
)


student_id = st.selectbox(
    "Select Student",
    data["Student_ID"].astype(str)
)


student = data[
    data["Student_ID"].astype(str)
    == student_id
].iloc[0]


# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.subheader(
    f"Student: {student_id}"
)


c1, c2, c3 = st.columns(3)


c1.metric(
    "Current GPA",
    f"{student['Current_GPA']:.2f}"
)

c2.metric(
    "Risk Probability",
    f"{student['Risk_Probability']:.1f}%"
)

c3.metric(
    "Risk Level",
    student["Risk_Level"]
)


st.divider()


# ------------------------------------------------
# ACADEMIC PROFILE
# ------------------------------------------------

st.subheader("Academic Profile")


c1, c2 = st.columns(2)


with c1:

    st.write(
        f"**Previous GPA:** "
        f"{student['Previous_GPA']:.2f}"
    )

    st.write(
        f"**Current GPA:** "
        f"{student['Current_GPA']:.2f}"
    )

    st.write(
        f"**GPA Trend:** "
        f"{student['GPA_Trend']:.2f}"
    )

    st.write(
        f"**Attendance:** "
        f"{student['Attendance_Rate']:.1f}%"
    )


with c2:

    st.write(
        f"**Assessment Average:** "
        f"{student['Assessment_Average']:.1f}%"
    )

    st.write(
        f"**Missing Assignments:** "
        f"{int(student['Missing_Assignments'])}"
    )

    st.write(
        f"**Study Activity:** "
        f"{student['Study_Activity']:.1f}"
    )


# ------------------------------------------------
# RISK FACTORS
# ------------------------------------------------

st.subheader(
    "Areas Requiring Review"
)


factors = identify_risk_factors(
    student
)


if factors:

    for factor in factors:

        st.warning(
            f"⚠️ {factor}"
        )

else:

    st.success(
        "No threshold-based concern was identified."
    )


# ------------------------------------------------
# CHART
# ------------------------------------------------

st.subheader(
    "Academic Indicators"
)


chart_data = {
    "Attendance": student["Attendance_Rate"],
    "Assessment": student["Assessment_Average"],
    "Study Activity": student["Study_Activity"],
}


st.bar_chart(chart_data)
