import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Ibnsina Pharma Equity Research", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    hist_data = {
        'Year': ['FY22', 'FY23', 'FY24', 'FY25E'],
        'Revenue (EGP Bn)': [22.26, 33.95, 55.84, 76.60],
        'Net Income (EGP Mn)': [0, 213.7, 614.5, 921.0],
        'Gross Margin (%)': [7.3, 7.4, 7.9, 8.1],
        'EBITDA Margin (%)': [3.0, 3.9, 4.5, 4.8]
    }
    forecast_data = {
        'Year': ['2026E', '2027E', '2028E', '2029E', '2030E'],
        'Growth (%)': [25, 22, 18, 15, 13],
        'EBITDA Margin (%)': [5.0, 5.2, 5.5, 5.8, 6.0]
    }
    sensitivity = pd.DataFrame({
        'WACC \ g': ['17.0%', '18.0%', '18.5%', '19.5%', '21.0%'],
        '5.5%': [23.8, 20.9, 19.7, 17.6, 15.2],
        '7.0%': [27.1, 23.5, 22.1, 19.6, 16.8],
        '8.5%': [31.2, 26.7, 25.0, 22.1, 18.7]
    })
    return pd.DataFrame(hist_data), pd.DataFrame(forecast_data), sensitivity

df_hist, df_fore, df_sens = get_data()

st.sidebar.title("Abdelrahim Elsweedy")
st.sidebar.markdown("### Recommendation: **BUY**")
st.sidebar.markdown("### Target Price: **EGP 20.0**")

st.title("📊 Ibnsina Pharma (ISPH.CA)")
st.subheader("Equity Research Dashboard")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Target Price", "EGP 20.0")
m2.metric("Upside Potential", "~85%")
m3.metric("Market Share", "30.8%")
m4.metric("WACC", "18.5%")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Historical Revenue (EGP Bn)")
    fig_rev = px.line(df_hist, x='Year', y='Revenue (EGP Bn)', text='Revenue (EGP Bn)', markers=True)
    st.plotly_chart(fig_rev, use_container_width=True)

with col2:
    st.markdown("### Margin Expansion Trend")
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['Gross Margin (%)'], name='Gross Margin'))
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['EBITDA Margin (%)'], name='EBITDA Margin'))
    st.plotly_chart(fig_margin, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Growth Forecast (%)")
    fig_fore = px.bar(df_fore, x='Year', y='Growth (%)')
    st.plotly_chart(fig_fore, use_container_width=True)

with col4:
    st.markdown("### DCF Sensitivity Table")
    st.table(df_sens.set_index('WACC \ g'))

st.caption("Disclaimer: Educational purposes only.")
