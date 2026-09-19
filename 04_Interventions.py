import streamlit as st
import pandas as pd
import os

from datetime import date

from utils import (
    load_data,
    load_model,
    prepare_predictions,
    identify_risk_factors
)


INTERVENTION_FILE = "data/interventions.csv"


st.title("🛠️ Intervention Management")


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


st.subheader(
    f"Support Plan — {student_id}"
)


st.write(
    f"Risk Level: **{student['Risk_Level']}**"
)

st.write(
    f"Risk Probability: "
    f"**{student['Risk_Probability']:.1f}%**"
)


factors = identify_risk_factors(
    student
)


if factors:

    st.write(
        "**Current areas requiring attention:**"
    )

    for factor in factors:

        st.write(
            f"• {factor}"
        )


st.divider()


st.subheader(
    "Create Intervention Plan"
)


actions = [
    "Teacher meeting",
    "Assignment catch-up plan",
    "Attendance monitoring",
    "Academic mentoring",
    "Extra academic support",
    "Parent/guardian communication",
    "Follow-up assessment"
]


selected_actions = []


for action in actions:

    if st.checkbox(
        action,
        key=f"{student_id}_{action}"
    ):

        selected_actions.append(action)


responsible_teacher = st.text_input(
    "Responsible teacher"
)


review_date = st.date_input(
    "Review date",
    value=date.today()
)


notes = st.text_area(
    "Intervention notes",
    height=150
)


if st.button(
    "💾 Save Intervention Plan"
):

    new_record = pd.DataFrame([
        {
            "Student_ID": student_id,
            "Date": str(date.today()),
            "Review_Date": str(review_date),
            "Responsible_Teacher":
                responsible_teacher,
            "Actions":
                "; ".join(selected_actions),
            "Notes":
                notes,
            "Status":
                "Active"
        }
    ])


    if os.path.exists(
        INTERVENTION_FILE
    ):

        old = pd.read_csv(
            INTERVENTION_FILE
        )

        updated = pd.concat(
            [old, new_record],
            ignore_index=True
        )

    else:

        updated = new_record


    updated.to_csv(
        INTERVENTION_FILE,
        index=False
    )


    st.success(
        "Intervention plan saved successfully."
    )


st.divider()


st.subheader(
    "Previous Intervention Records"
)


if os.path.exists(
    INTERVENTION_FILE
):

    history = pd.read_csv(
        INTERVENTION_FILE
    )


    student_history = history[
        history["Student_ID"].astype(str)
        == student_id
    ]


    if not student_history.empty:

        st.dataframe(
            student_history,
            use_container_width=True
        )

    else:

        st.info(
            "No intervention history exists for this student."
        )

else:

    st.info(
        "No intervention records have been created yet."
    )
