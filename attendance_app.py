
import streamlit as st
import pandas as pd
from teacher_entry import teacher_attendance_entry

st.set_page_config(page_title="BSB Attendance Dashboard", layout="wide")

@st.cache_data
def load_data():
    students = pd.read_csv("data/students.csv")
    attendance = pd.read_csv("data/attendance.csv", parse_dates=['date'])
    teachers = pd.read_csv("data/teachers.csv")
    return students, attendance, teachers

def main():
    students, attendance, teachers = load_data()

    if students.empty:
        st.error("Student list not found.")
        return

    st.sidebar.title("Select View Mode")
    mode = st.sidebar.radio("View Mode", ["Teacher", "Admin"])

    if mode == "Teacher":
        teacher_attendance_entry(students, attendance, teachers)
    else:
        st.title("📊 BSB Attendance Dashboard")

        total_students = len(students)
        st.subheader("📚 Attendance Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", total_students)

        attendance_rate = (
            len(attendance[attendance["status"] == "P"]) / len(attendance)
            if not attendance.empty else 0
        )
        col2.metric("Attendance Rate", f"{attendance_rate:.1%}")

        girls = students[students["gender"] == "F"]
        girls_pct = len(girls) / total_students if total_students > 0 else 0
        col3.metric("Girls %", f"{girls_pct:.1%}")

        if "class" in attendance.columns:
            absences_by_class = (
                attendance[attendance["status"].isin(["E", "U"])]
                .groupby("class").size().sort_values(ascending=False)
            )
            most_absent_class = absences_by_class.idxmax() if not absences_by_class.empty else "N/A"
            col4.metric("Most Absent Class", most_absent_class)
        else:
            col4.metric("Most Absent Class", "N/A")
            st.warning("⚠️ Attendance file does not include a 'class' column. Cannot filter by class.")

if __name__ == "__main__":
    main()
