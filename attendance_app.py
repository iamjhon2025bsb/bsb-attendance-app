
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="BSB Attendance Dashboard", layout="wide")

@st.cache_data
def load_data():
    # Load student data from master Excel file
    master_df = pd.read_csv("data/students_master.csv")

    # Standardize column names and select relevant ones
    students = master_df.rename(columns={
        "Student ID": "student_id",
        "Name": "name",
        "Class": "class",
        "Gender": "gender",
        "House": "house"
    })[["student_id", "name", "class", "gender", "house"]]

    students = students.dropna(subset=["student_id"])
    students.columns = students.columns.str.strip()

    # Load attendance data
    attendance = pd.read_csv("data/attendance.csv", parse_dates=["date"])
    attendance.columns = attendance.columns.str.strip()

    # Load teacher data
    teachers = pd.read_csv("data/teachers.csv")
    teachers.columns = teachers.columns.str.strip()

    return students, attendance, teachers

students, attendance, teachers = load_data()

st.title("BSB Attendance System")

view = st.sidebar.selectbox("Choose your view:", ["Admin Panel", "Teacher Panel"])

if view == "Admin Panel":
    st.header("Admin Dashboard")

    # Show overall stats
    total_students = len(students)
    total_classes = students["class"].nunique()
    total_attendance = len(attendance)

    st.metric("Total Students", total_students)
    st.metric("Classes", total_classes)
    st.metric("Attendance Records", total_attendance)

    # Optional breakdowns
    st.subheader("House Distribution")
    st.dataframe(students["house"].value_counts())

elif view == "Teacher Panel":
    st.header("Teacher Dashboard")

    teacher_names = teachers["teacher_name"].unique()
    selected_teacher = st.selectbox("Select your name", teacher_names)

    # Identify teacher's class
    teacher_class = teachers[teachers["teacher_name"] == selected_teacher]["class"].values[0]

    st.success(f"Welcome, {selected_teacher} - Class: {teacher_class}")

    # Filter students and attendance
    class_students = students[students["class"] == teacher_class]
    class_attendance = attendance[attendance["class"] == teacher_class]

    # Display
    st.subheader("Students in Your Class")
    st.dataframe(class_students)

    st.subheader("Recent Attendance")
    st.dataframe(class_attendance.tail(10))
