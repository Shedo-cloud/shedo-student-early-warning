import streamlit as st
import pandas as pd

from utils import (
    load_data,
    load_model,
    prepare_predictions,
    identify_risk_factors
)


st.title("📝 Parent/Guardian Reports")


data = load_data()
model = load_model()

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


teacher_notes = st.text_area(
    "Teacher observations",
    height=150
)


report_style = st.selectbox(
    "Report style",
    [
        "Formal school report",
        "Friendly parent message",
        "Short communication"
    ]
)


if st.button(
    "Generate Report"
):

    factors = identify_risk_factors(
        student
    )


    if factors:

        concerns = ", ".join(
            factors
        )

    else:

        concerns = (
            "No major threshold-based "
            "concerns were identified."
        )


    if report_style == "Formal school report":

        report = f"""
Dear Parent/Guardian,

We are writing to provide an update regarding the
academic progress of your child (Student ID: {student_id}).

The student's current GPA is {student['Current_GPA']:.2f},
compared with a previous GPA of
{student['Previous_GPA']:.2f}.

The current academic indicators suggest that the
following areas may benefit from additional attention:

{concerns}

The school is reviewing appropriate academic support
measures and will continue monitoring the student's
progress.

Teacher observations:

{teacher_notes}

We value your partnership with the school and welcome
your support in helping the student maintain positive
academic progress.

Yours sincerely,

Academic Support Team
"""

    elif report_style == "Friendly parent message":

        report = f"""
Dear Parent/Guardian,

We would like to share a brief update about
Student {student_id}'s academic progress.

The student's current GPA is
{student['Current_GPA']:.2f}.

Some areas that may benefit from additional attention
include: {concerns}.

The school is working to provide appropriate support,
and we would appreciate your partnership as we continue
to monitor progress.

Teacher notes:

{teacher_notes}

Thank you for your continued support.
"""

    else:

        report = f"""
Dear Parent/Guardian,

We would like to discuss Student {student_id}'s
current academic progress.

Areas for attention include:
{concerns}

The school is putting appropriate support measures
in place and will continue monitoring progress.

Thank you.
"""


    st.subheader(
        "Generated Report"
    )


    edited_report = st.text_area(
        "Review and edit before sending",
        value=report,
        height=400
    )


    st.download_button(
        "📥 Download Report",
        data=edited_report,
        file_name=f"{student_id}_parent_report.txt",
        mime="text/plain"
    )
