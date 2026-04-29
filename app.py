import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Ibnsina Pharma Equity Research", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] > div {
        color: white !important;
    }
    [data-testid="stMetricLabel"] > div {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    [data-testid="stMetricDelta"] > div {
        color: #00ff00 !important;
    }
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3a3f5a;
    }
    .green-buy {
        color: #00ff00;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def get_static_data():
    hist_data = {
        'Year': ['FY22', 'FY23', 'FY24', 'FY25E'],
        'Revenue (EGP Bn)': [22.26, 33.95, 55.84, 76.60],
        'Gross Margin (%)': [7.3, 7.4, 7.9, 8.1],
        'EBITDA Margin (%)': [3.0, 3.9, 4.5, 4.8]
    }
    forecast_data = {
        'Year': ['2026E', '2027E', '2028E', '2029E', '2030E'],
        'Growth (%)': [25, 22, 18, 15, 13]
    }
    sensitivity_df = pd.DataFrame({
        'WACC \\ g': ['17.0%', '18.0%', '18.5%', '19.5%', '21.0%'],
        '5.5%': [23.8, 20.9, 19.7, 17.6, 15.2],
        '7.0%': [27.1, 23.5, 22.1, 19.6, 16.8],
        '8.5%': [31.2, 26.7, 25.0, 22.1, 18.7]
    })
    return pd.DataFrame(hist_data), pd.DataFrame(forecast_data), sensitivity_df

def calculate_dynamic_price(wacc):
    base_price = 22.1
    base_wacc = 18.5 / 100
    sensitivity_factor = 20.0 
    wacc_decimal = wacc / 100
    wacc_difference = wacc_decimal - base_wacc
    dynamic_price = base_price * (1 - (wacc_difference * sensitivity_factor))
    current_price_proxy = 11.0
    upside = ((dynamic_price / current_price_proxy) - 1) * 100
    return np.round(dynamic_price, 1), np.round(upside, 0)

df_hist, df_fore, df_sens = get_static_data()

st.sidebar.markdown(f"## Abdelrahim Elsweedy, FMVA")
st.sidebar.markdown(f"Recommendation: <span class='green-buy'>BUY</span>", unsafe_allow_html=True)
st.sidebar.divider()
st.sidebar.subheader("Valuation Assumptions")
selected_wacc = st.sidebar.slider(
    "Adjust WACC (%)",
    min_value=17.0,
    max_value=21.0,
    value=18.5,
    step=0.1
)

dynamic_target, dynamic_upside = calculate_dynamic_price(selected_wacc)
st.sidebar.metric(label="Dynamic Target Price", value=f"EGP {dynamic_target}", delta=f"{dynamic_upside}% Upside")
st.sidebar.divider()

st.title("Ibnsina Pharma (ISPH.CA)")
st.subheader("Equity Research Dashboard")

m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Target Price (Dynamic)", value=f"EGP {dynamic_target}")
m2.metric(label="Upside Potential", value=f"~{dynamic_upside}%", delta=f"{dynamic_upside}%")
m3.metric(label="Market Share (FY24)", value="30.8%")
m4.metric(label="Selected WACC", value=f"{selected_wacc}%")

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Historical Revenue (EGP Bn)")
    fig_rev = px.line(df_hist, x='Year', y='Revenue (EGP Bn)', markers=True, template="plotly_dark")
    fig_rev.update_traces(line_color='#1f77b4')
    st.plotly_chart(fig_rev, use_container_width=True)

with col2:
    st.markdown("### Margin Expansion Trend")
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['Gross Margin (%)'], name='Gross Margin'))
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['EBITDA Margin (%)'], name='EBITDA Margin'))
    fig_margin.update_layout(template="plotly_dark", legend_orientation="h")
    st.plotly_chart(fig_margin, use_container_width=True)

st.divider()

col3, col4 = st.columns([1, 1])
with col3:
    st.markdown("### Growth Forecast (%)")
    fig_fore = px.bar(df_fore, x='Year', y='Growth (%)', template="plotly_dark")
    st.plotly_chart(fig_fore, use_container_width=True)

with col4:
    st.markdown("### DCF Sensitivity Table (Static Report Data)")
    st.table(df_sens.set_index('WACC \\ g'))

st.divider()
st.caption("Disclaimer: This dashboard is for illustrative educational purposes only.")
