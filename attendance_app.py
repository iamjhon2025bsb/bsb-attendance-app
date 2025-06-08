
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="BSB Attendance App", layout="wide")

st.title("📊 BSB Attendance Dashboard")

# Safely load student data
students_path = "data/students.csv"
attendance_path = "data/attendance.csv"

def safe_read_csv(path, label):
    if not os.path.exists(path):
        st.warning(f"{label} file not found at `{path}`.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        if df.empty:
            st.info(f"{label} is empty.")
        return df
    except Exception as e:
        st.error(f"Error reading {label}: {e}")
        return pd.DataFrame()

students_df = safe_read_csv(students_path, "Student list")
attendance_df = safe_read_csv(attendance_path, "Attendance records")

if not students_df.empty:
    st.success(f"Loaded {len(students_df)} students.")
    st.dataframe(students_df.head())
else:
    st.stop()

if not attendance_df.empty:
    st.success(f"Loaded {len(attendance_df)} attendance records.")
    st.dataframe(attendance_df.head())
