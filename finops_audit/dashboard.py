import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="FinOps Audit Dashboard", layout="wide")
st.title("☁️ Cloud FinOps: Zombie Asset Audit")

# 2. Mock Data (Simulating the output of your finops_optimizer.py)
# In the future, we will connect this directly to your MongoDB
data = {
    "Instance ID": ["ZOMBIE-999", "ZOMBIE-102", "ZOMBIE-405"],
    "CPU Usage (%)": [1.2, 0.8, 2.1],
    "Daily Cost ($)": [650.0, 520.0, 710.0]
}
df = pd.DataFrame(data)

# 3. KPI Metrics
col1, col2, col3 = st.columns(3)
total_waste = df["Daily Cost ($)"].sum()
col1.metric("Zombie Assets Found", len(df))
col2.metric("Daily Cost Leakage", f"${total_waste:,.2f}")
col3.metric("Annualized Savings Potential", f"${total_waste * 365:,.2f}")

# 4. Data Table
st.subheader("Idle Resource Breakdown")
st.table(df)

# 5. Visual Insight
st.subheader("Cost Impact Visualization")
st.bar_chart(df.set_index("Instance ID")["Daily Cost ($)"])