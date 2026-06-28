import streamlit as st
import pandas as pd
from engine import DBConnector

# 1. Page Config
st.set_page_config(page_title="Retail Media Analytics", layout="wide")
st.title("📈 Retail Media: Performance & ROAS Matrix")

# 2. Data Fetching
@st.cache_resource
def get_campaign_data():
    db = DBConnector()
    if not db.connect(): return pd.DataFrame()
    data = list(db.db["retail_media"].find({}))
    db.close()
    return pd.DataFrame(data)

df = get_campaign_data()

if not df.empty:
    # 3. Process ROAS (Logic from your script)
    df['roas'] = (df['in_store_checkout_lift'] * 100000) / df['digital_ad_spend']
    
    # 4. KPI Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Campaigns", len(df))
    col2.metric("Avg ROAS", f"${df['roas'].mean():.2f}")
    col3.metric("Underperforming", len(df[df['roas'] < 2.0]))

    # 5. Visualization: ROAS by Channel
    st.subheader("ROAS Performance by Channel")
    st.bar_chart(df.groupby('channel')['roas'].mean())
    
    # 6. Detailed Data Table
    st.dataframe(df[['campaign_id', 'channel', 'digital_ad_spend', 'roas']])
else:
    st.warning("No retail media data found.")