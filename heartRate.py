import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Streamlit Page Setup
st.set_page_config(page_title="Heart Rate & Sensor Dashboard", layout="wide")
st.title("🫀 Patient & Environmental Sensor Data")

# Database Credentials
DB_HOST = "82.180.143.66"
DB_USER = "u263681140_students"
DB_PASS = "testStudents@123"
DB_NAME = "u263681140_students"
DB_PORT = 3306

@st.cache_data(ttl=5)  # Auto-refresh cache every 5 seconds
def load_data():
    connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_url)
    query = "SELECT * FROM heart_rate ORDER BY Date_Time DESC"
    
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

# Fetch Data
try:
    df = load_data()

    if not df.empty:
        # Display Latest Metrics
        latest = df.iloc[0]
        st.subheader("Latest Readings")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Body Temp (°F/°C)", f"{latest['Body_temp']:.1f}")
        col2.metric("Oxygen (SpO2 %)", f"{latest['Oxygen']:.1f}%")
        col3.metric("Heart Rate (BPM)", f"{latest['Heart_Rate']:.0f}")
        col4.metric("Room Temp (°C)", f"{latest['Temp']:.1f}")
        col5.metric("Humidity (%)", f"{latest['Humi']:.1f}%")

        st.divider()

        # Graphs Section
        st.subheader("Vitals Trends")
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.write("**Heart Rate & Oxygen**")
            st.line_chart(df.set_index("Date_Time")[["Heart_Rate", "Oxygen"]])

        with chart_col2:
            st.write("**Body & Room Temperature**")
            st.line_chart(df.set_index("Date_Time")[["Body_temp", "Temp"]])

        st.divider()

        # Raw Data Table
        st.subheader("All Records")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No data found in the `heart_rate` table.")

except Exception as e:
    st.error(f"Error connecting to the database: {e}")

# Manual Refresh Button
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
