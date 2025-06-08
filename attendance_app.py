
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="📚 BSB Attendance", layout="wide")

st.title("📚 BSB Attendance Tracker")

# Display an indicator that app is loading
st.markdown("🔄 Loading data files...")

def safe_read_csv(path, label):
    if not os.path.exists(path):
        st.warning(f"⚠️ `{path}` not found for {label}.")
        return pd.DataFrame()
    try:
        df = pd.read_csv(path)
        if df.empty:
            st.info(f"ℹ️ {label} is empty.")
        return df
    except Exception as e:
        st.error(f"❌ Failed to read {label}: {e}")
        return pd.DataFrame()

# Load files with visible feedback
students_df = safe_read_csv("data/students.csv", "Students")
attendance_df = safe_read_csv("data/attendance.csv", "Attendance")

# Display data or placeholder info
if not students_df.empty:
    st.success(f"✅ Loaded {len(students_df)} students.")
    st.dataframe(students_df)
else:
    st.warning("⚠️ No student data to display.")

if not attendance_df.empty:
    st.success(f"✅ Loaded {len(attendance_df)} attendance records.")
    st.dataframe(attendance_df)
else:
    st.info("ℹ️ No attendance records available.")
