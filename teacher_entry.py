import streamlit as st
import pandas as pd
from datetime import date
import os

# ---------------------- CONFIG ----------------------
STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"
ATTENDANCE_STATUSES = ["P", "T", "E", "U"]

# ---------------------- LOAD STUDENTS ----------------------
def load_students():
    if not os.path.exists(STUDENT_FILE):
        st.error("Student list not found.")
        return pd.DataFrame()
    df = pd.read_csv(STUDENT_FILE)
    df.dropna(subset=["student_id", "full_name", "class"], inplace=True)
    return df

# ---------------------- MAIN ENTRY ----------------------
def teacher_attendance_entry():
    st.title("📋 Teacher Attendance Entry")
    students_df = load_students()
    if students_df.empty:
        return

    # Step 1: Teacher selects class
    teacher_class = st.selectbox("Select Your Class", sorted(students_df["class"].unique()))
    class_students = students_df[students_df["class"] == teacher_class].copy()

    # Step 2: Select date
    selected_date = st.date_input("Select Date", value=date.today())

    # Step 3: Mark attendance
    st.markdown("### ✏️ Mark Attendance")
    attendance_data = []

    for _, row in class_students.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{row['full_name']}**")
        with col2:
            status = st.selectbox("Status", ATTENDANCE_STATUSES, key=row['student_id'])
        attendance_data.append({
            "student_id": row['student_id'],
            "date": selected_date,
            "status": status,
            "term": detect_term(selected_date)  # Assumes a function for term detection
        })

    # Step 4: Submit button
    if st.button("✅ Submit Attendance"):
        save_attendance(attendance_data)
        st.success("Attendance submitted successfully!")

# ---------------------- TERM DETECTION ----------------------
def detect_term(selected_date):
    if date(selected_date.year, 8, 1) <= selected_date <= date(selected_date.year, 12, 31):
        return "Term 1"
    elif date(selected_date.year, 1, 1) <= selected_date <= date(selected_date.year, 4, 15):
        return "Term 2"
    else:
        return "Term 3"

# ---------------------- SAVE LOGIC ----------------------
def save_attendance(entries):
    if os.path.exists(ATTENDANCE_FILE):
        existing = pd.read_csv(ATTENDANCE_FILE, parse_dates=["date"])
        new_entries = pd.DataFrame(entries)
        combined = pd.concat([existing, new_entries], ignore_index=True)
    else:
        combined = pd.DataFrame(entries)
    combined.to_csv(ATTENDANCE_FILE, index=False)

# ---------------------- RUN ----------------------
teacher_attendance_entry()
