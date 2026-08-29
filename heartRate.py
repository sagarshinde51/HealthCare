import streamlit as st
import pandas as pd
import mysql.connector

# Page Configuration
st.set_page_config(page_title="Heart Rate & Sensor Dashboard", layout="wide")
st.title("🫀 Sensor Data Monitor (MySQL)")

# Database Credentials
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students",
    "password": "testStudents@123",
    "database": "u263681140_students",
    "port": 3306
}

@st.cache_data(ttl=5)  # Cache refreshes every 5 seconds
def load_data():
    conn = mysql.connector.connect(**DB_CONFIG)
    query = "SELECT * FROM heart_rate ORDER BY Date_Time DESC"
    
    # Read directly into a DataFrame
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch and display data
try:
    df = load_data()

    if not df.empty:
        # Latest Readings Metrics
        latest = df.iloc[0]
        st.subheader("Latest Readings")
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Body Temp", f"{float(latest['Body_temp']):.1f}")
        col2.metric("Oxygen (SpO2)", f"{float(latest['Oxygen']):.1f}%")
        col3.metric("Heart Rate", f"{float(latest['Heart_Rate']):.0f} BPM")
        col4.metric("Room Temp", f"{float(latest['Temp']):.1f}°C")
        col5.metric("Humidity", f"{float(latest['Humi']):.1f}%")

        st.divider()

        # Trend Charts
        st.subheader("Vitals Trends")
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("**Heart Rate & Oxygen Level**")
            st.line_chart(df.set_index("Date_Time")[["Heart_Rate", "Oxygen"]])

        with chart_col2:
            st.write("**Body Temp vs Room Temp**")
            st.line_chart(df.set_index("Date_Time")[["Body_temp", "Temp"]])

        st.divider()

        # Data Table
        st.subheader("Recorded History")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("Table `heart_rate` is currently empty.")

except mysql.connector.Error as e:
    st.error(f"MySQL Connection Error: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")

# Manual Refresh Button
if st.button("Refresh Now"):
    st.cache_data.clear()
    st.rerun()
