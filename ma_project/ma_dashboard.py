import streamlit as st
import pandas as pd
from engine import DBConnector

# 1. Page Config
st.set_page_config(page_title="M&A Due Diligence", layout="wide")
st.title("💼 M&A Due Diligence: Revenue Attrition Tracker")

# 2. Data Fetching
@st.cache_resource
def get_deal_data():
    db = DBConnector()
    if not db.connect(): return pd.DataFrame()
    data = list(db.db["ma_deals"].find({}))
    db.close()
    return pd.DataFrame(data)

df = get_deal_data()

if not df.empty:
    # 3. KPI Metrics
    total_mrr = sum(d['mrr'] for d in df['financials'])
    high_risk_deals = df[df['risk_score'] > 60]
    revenue_at_risk = high_risk_deals['financials'].apply(lambda x: x['mrr']).sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Deal MRR", f"${total_mrr:,.2f}")
    col2.metric("Revenue at Risk", f"${revenue_at_risk:,.2f}", delta_color="inverse")
    col3.metric("High-Risk Count", len(high_risk_deals))

    # 4. Visuals
    st.subheader("Risk Distribution")
    st.scatter_chart(df, x='risk_score', y='financials', size=20)
    
    st.subheader("High-Risk Alerts")
    st.dataframe(high_risk_deals[['customer_id', 'risk_score', 'support_log']])
else:
    st.warning("No deal data found.")