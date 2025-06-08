
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BSB Attendance Dashboard", layout="wide")

@st.cache_data
def load_data():
    students = pd.read_csv("data/students.csv")
    attendance = pd.read_csv("data/attendance.csv", parse_dates=['date'])
    return students, attendance

students, attendance = load_data()

st.title("📊 BSB Attendance Dashboard")

view_mode = st.radio("Select View Mode", ["Teacher", "Admin"], horizontal=True)

classes = sorted(students["class"].dropna().unique())
selected_class = None
if view_mode == "Teacher":
    selected_class = st.selectbox("Select your class", classes)
    students = students[students["class"] == selected_class]
    attendance = attendance[attendance["class"] == selected_class]

terms = sorted(attendance["term"].dropna().unique())
selected_term = st.selectbox("Select Term", terms)
attendance = attendance[attendance["term"] == selected_term]

merged = pd.merge(attendance, students, on="student_id", how="left")

st.markdown("### 🔍 Attendance Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Students", students.shape[0])
with col2:
    total_attendance = attendance.shape[0]
    present_count = attendance[attendance["status"].isin(["P", "T"])].shape[0]
    percent_present = (present_count / total_attendance * 100) if total_attendance else 0
    st.metric("Attendance Rate", "{:.1f}%".format(percent_present))
with col3:
    gender_ratio = students["gender"].value_counts(normalize=True) * 100
    st.metric("Girls %", "{:.1f}%".format(gender_ratio.get("F", 0)))
with col4:
    absences_by_class = merged[merged["status"].isin(["E", "U"])].groupby("class").size()
    most_absent_class = absences_by_class.idxmax() if not absences_by_class.empty else "N/A"
    st.metric("Most Absent Class", most_absent_class)

st.markdown("### 🚨 Top Absentees")
absent_count = merged[merged["status"].isin(["E", "U"])].groupby(["student_id", "name", "class"]).size().reset_index(name="absences")
top_absentees = absent_count.sort_values(by="absences", ascending=False).head(5)
st.dataframe(top_absentees)

st.markdown("### 🏠 House Overview")
house_stats = merged[merged["status"].isin(["P", "T", "E", "U"])]
house_summary = house_stats.groupby("house")["status"].value_counts().unstack().fillna(0)
house_summary["Total Records"] = house_summary.sum(axis=1)
house_summary["% Present"] = (
    house_summary.get("P", 0) + house_summary.get("T", 0)
) / house_summary["Total Records"] * 100
st.dataframe(house_summary[["Total Records", "% Present"]].sort_values(by="% Present", ascending=False))

st.markdown("### 🧾 Student List")
st.dataframe(students)

st.markdown("### 🕓 Attendance Records")
st.dataframe(attendance)
