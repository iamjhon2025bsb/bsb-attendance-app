
from teacher_entry import teacher_attendance_entry
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BSB Attendance Dashboard", layout="wide")

@st.cache_data
def load_data():
    students = pd.read_csv("data/students.csv")
    attendance = pd.read_csv("data/attendance.csv", parse_dates=['date'])
    teachers = pd.read_csv("data/teachers.csv")
    return students, attendance, teachers

def preprocess_data(students, attendance):
    # Merge student info into attendance
    merged = pd.merge(attendance, students, on="student_id", how="left", suffixes=("_att", "_stu"))

    # Fill class from student data if attendance class is unknown
    if "class_att" in merged.columns and "class_stu" in merged.columns:
        merged["class"] = merged["class_att"].where(merged["class_att"] != "Unknown", merged["class_stu"])
    elif "class" not in merged.columns:
        st.warning("Merged data missing 'class' info. Analysis may be limited.")

    return merged

def main():
    students, attendance, teachers = load_data()
    merged = preprocess_data(students, attendance)

    view_mode = st.radio("Select View Mode", ["Teacher", "Admin"], horizontal=True)

    if view_mode == "Teacher":
        teacher_attendance_entry(students, attendance, teachers)
    else:
        st.header("📊 Attendance Summary")
        st.metric("Total Students", len(students))
        st.metric("Attendance Rate", f"{100 * merged['status'].isin(['P']).mean():.1f}%" if not merged.empty else "0.0%")
        st.metric("Girls %", f"{100 * (students['gender'] == 'F').mean():.1f}%" if not students.empty else "0.0%")

        try:
            absences_by_class = merged[merged["status"].isin(["E", "U"])].groupby("class").size()
            st.subheader("🚫 Top Absentees by Class")
            st.bar_chart(absences_by_class)
        except KeyError as e:
            st.error(f"Missing expected column during analysis: {e}")

if __name__ == "__main__":
    main()
