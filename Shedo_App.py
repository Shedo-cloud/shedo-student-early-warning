import streamlit as st

st.set_page_config(
    page_title="Shedo Student Early-Warning System",
    page_icon="🎓",
    layout="wide"
)

dashboard = st.Page(
    "01_Dashboard.py",
    title="Dashboard",
    icon="📊"
)

students = st.Page(
    "02_Student_Profiles.py",
    title="Student Profiles",
    icon="👨‍🎓"
)

at_risk = st.Page(
    "03_At_Risk_Students.py",
    title="At-Risk Students",
    icon="⚠️"
)

interventions = st.Page(
    "04_Interventions.py",
    title="Interventions",
    icon="🛠️"
)

parent_reports = st.Page(
    "05_Parent_Reports.py",
    title="Parent Reports",
    icon="📝"
)

downloads = st.Page(
    "06_Reports_Downloads.py",
    title="Reports & Downloads",
    icon="📥"
)

pg = st.navigation({
    "Academic Monitoring": [
        dashboard,
        students,
        at_risk,
    ],
    "Student Support": [
        interventions,
        parent_reports,
    ],
    "Reports": [
        downloads,
    ],
})

pg.run()
