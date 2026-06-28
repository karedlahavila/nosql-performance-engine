import streamlit as st
import pandas as pd
from engine import DBConnector

# 1. Page Config
st.set_page_config(page_title="Aviation Friction Analysis", layout="wide")
st.title("✈️ Aviation Network: Friction & Delay Analysis")

# 2. Data Fetching
@st.cache_resource
def get_flight_data():
    db = DBConnector()
    if not db.connect():
        return pd.DataFrame()
    data = db.query_records("flights", {})
    db.close()
    return pd.DataFrame(data)

df = get_flight_data()

if not df.empty:
    # 3. Process Friction Index
    def calculate_friction(row):
        metrics = row['operational_metrics']
        impact = row['passenger_impact']
        return (metrics['delay_minutes'] * 0.7) + (impact['tight_connections'] * 0.3)

    df['friction_index'] = df.apply(calculate_friction, axis=1)

    # 4. KPI Metrics
    col1, col2, col3 = st.columns(3)
    high_friction = df[df['friction_index'] > 30]
    col1.metric("Total Flights", len(df))
    col2.metric("Priority Alerts", len(high_friction))
    col3.metric("Avg Friction Index", f"{df['friction_index'].mean():.2f}")

    # 5. Visuals
    st.subheader("Friction Heatmap by Origin")
    st.bar_chart(df.groupby('origin')['friction_index'].mean())
    
    st.subheader("Flight-by-Flight Friction Detail")
    st.dataframe(df[['flight_id', 'origin', 'friction_index']])
else:
    st.error("No flight data found. Run your aviation_generator.py first!")