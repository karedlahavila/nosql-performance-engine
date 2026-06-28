import streamlit as st
import pandas as pd
from engine import DBConnector

# 1. Page Config
st.set_page_config(page_title="Specialty Drug Access", layout="wide")
st.title("💊 Specialty Drug: Onboarding & Access Tracker")

# 2. Database Connection
@st.cache_resource
def get_onboarding_data():
    db_helper = DBConnector()
    if not db_helper.connect():
        return pd.DataFrame()
    # Fetch all records from the funnel
    data = list(db_helper.db["onboarding_funnel"].find({}))
    db_helper.close()
    return pd.DataFrame(data)

df = get_onboarding_data()

if not df.empty:
    # 3. KPI Metrics
    col1, col2, col3 = st.columns(3)
    denied = df[df['status'] == "Denied"]
    col1.metric("Total Patients", len(df))
    col2.metric("Denied/Action Required", len(denied))
    col3.metric("Approval Rate", f"{((len(df)-len(denied))/len(df))*100:.1f}%")

    # 4. Visualization: Denial Reason Breakdown
    st.subheader("Analysis of Denials")
    if not denied.empty:
        st.bar_chart(denied['denial_reason'].value_counts())
    
    # 5. Patient Tracking Table
    st.subheader("Patient Access Log")
    st.dataframe(df[['patient_id', 'drug_name', 'status', 'denial_reason']])
else:
    st.warning("No onboarding records found. Run the access tracker script first!")