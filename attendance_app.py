
import streamlit as st
import pandas as pd

def load_data():
    students = pd.read_csv("data/students_master.csv")
    attendance = pd.read_csv("data/attendance.csv")
    teachers = pd.read_csv("data/teachers.csv")
    return students, attendance, teachers

students, attendance, teachers = load_data()

st.title("📊 BSB Attendance Dashboard (Minimal Version)")

st.subheader("👨‍🎓 Students Preview")
st.dataframe(students.head())

st.subheader("🗓️ Attendance Preview")
st.dataframe(attendance.head())

st.subheader("👩‍🏫 Teachers Preview")
st.dataframe(teachers.head())
