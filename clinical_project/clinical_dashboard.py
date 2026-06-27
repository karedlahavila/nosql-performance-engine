import streamlit as st
import pandas as pd
from pymongo import MongoClient

# 1. Page Config
st.set_page_config(page_title="Clinical Revenue Integrity", layout="wide")
st.title("🏥 Clinical Revenue Integrity: Audit & Adjudication")

# 2. Database Connection
@st.cache_resource
def get_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["portfolio_engine"]
    return list(db["audited_reporting_claims"].find({}))

data = get_data()
df = pd.DataFrame(data)

# Flattening the nested Mongo structure for easy viewing
df['risk_score'] = df['audit_assessment'].apply(lambda x: x['pre_payment_risk_score_pct'])
df['status'] = df['audit_assessment'].apply(lambda x: x['auditor_status'])
df['duration'] = df['independent_telemetry'].apply(lambda x: x['verified_room_duration_minutes'])
df['billed_amount'] = df['billing_claim_submitted'].apply(lambda x: x['charged_amount'])

# 3. KPI Metrics
col1, col2, col3 = st.columns(3)
flagged = df[df['status'] == "Diverted to Human Auditor"]
col1.metric("Claims Flagged for Review", len(flagged))
col2.metric("Leakage Prevented", f"${flagged['billed_amount'].sum():,.2f}")
col3.metric("Auto-Approval Rate", f"{((len(df)-len(flagged))/len(df))*100:.1f}%")

# 4. Interactive Charts
st.subheader("High-Risk Claims: Duration vs. Complexity")
st.scatter_chart(data=df, x='duration', y='risk_score', color='status')

# 5. Data Table
st.subheader("Audited Claims Detail")
st.dataframe(df[['patient_name', 'risk_score', 'status', 'duration', 'billed_amount']])