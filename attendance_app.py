
import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    students = pd.read_csv("data/students.csv")
    attendance = pd.read_csv("data/attendance.csv")
    teachers = pd.read_csv("data/teachers.csv")
    return students, attendance, teachers

students, attendance, teachers = load_data()

# App title and intro
st.title("📘 BSB Attendance Dashboard")
st.markdown("Select your role to proceed:")

# Role selection
role = st.selectbox("Login as", ["Admin", "Teacher"])

if role == "Admin":
    st.header("📊 Admin Dashboard")
    st.subheader("👨‍🎓 Student Records")
    st.dataframe(students)

    st.subheader("🗓️ Attendance Records")
    st.dataframe(attendance)

    st.subheader("👩‍🏫 Teachers List")
    st.dataframe(teachers)

elif role == "Teacher":
    teacher_name = st.selectbox("Select your name", teachers["name"].unique())
    teacher_class = teachers.loc[teachers["name"] == teacher_name, "class"].values[0]

    st.header(f"📋 {teacher_name}'s Attendance Panel")
    st.markdown(f"Showing students in class: `{teacher_class}`")

    class_students = students[students["class"] == teacher_class]
    st.dataframe(class_students)

    class_attendance = attendance[attendance["class"] == teacher_class]
    st.dataframe(class_attendance)
