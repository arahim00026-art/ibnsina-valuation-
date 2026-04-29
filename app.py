import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Ibnsina Pharma Report", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    [data-testid="stMetricValue"] > div { color: white !important; font-size: 1.8rem !important; }
    [data-testid="stMetricLabel"] > div { color: rgba(255, 255, 255, 0.8) !important; }
    [data-testid="stMetricDelta"] > div { color: #00ff00 !important; }
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #3a3f5a;
    }
    .green-buy { color: #00ff00; font-weight: bold; }
    .stTable { font-size: 0.8rem !important; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
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
        'Year': ['26E', '27E', '28E', '29E', '30E'],
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
    base_price, base_wacc, sensitivity_factor = 22.1, 0.185, 20.0
    wacc_diff = (wacc / 100) - base_wacc
    dynamic_price = base_price * (1 - (wacc_diff * sensitivity_factor))
    upside = ((dynamic_price / 11.0) - 1) * 100
    return np.round(dynamic_price, 1), np.round(upside, 0)

df_hist, df_fore, df_sens = get_static_data()

st.sidebar.markdown(f"## Abdelrahim Elsweedy, FMVA")
st.sidebar.markdown(f"Rec: <span class='green-buy'>BUY</span>", unsafe_allow_html=True)
selected_wacc = st.sidebar.slider("WACC (%)", 17.0, 21.0, 18.5, 0.1)
dynamic_target, dynamic_upside = calculate_dynamic_price(selected_wacc)
st.sidebar.metric("Target Price", f"EGP {dynamic_target}", f"{dynamic_upside}% Upside")

st.title("Ibnsina Pharma (ISPH.CA)")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Target (Dyn)", f"EGP {dynamic_target}")
m2.metric("Upside", f"{dynamic_upside}%")
m3.metric("Mkt Share", "30.8%")
m4.metric("WACC", f"{selected_wacc}%")

st.write("---")

c1, c2 = st.columns(2)
with c1:
    fig_rev = px.line(df_hist, x='Year', y='Revenue (EGP Bn)', markers=True, template="plotly_dark", height=250)
    fig_rev.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['Gross Margin (%)'], name='GM'))
    fig_margin.add_trace(go.Scatter(x=df_hist['Year'], y=df_hist['EBITDA Margin (%)'], name='EBITDA'))
    fig_margin.update_layout(template="plotly_dark", height=250, margin=dict(l=0, r=0, t=30, b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02))
    st.plotly_chart(fig_margin, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    fig_fore = px.bar(df_fore, x='Year', y='Growth (%)', template="plotly_dark", height=250)
    fig_fore.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_fore, use_container_width=True)

with c4:
    st.markdown("<p style='font-size:0.9rem; font-weight:bold; margin-bottom:5px;'>Sensitivity Table</p>", unsafe_allow_html=True)
    st.table(df_sens.set_index('WACC \\ g'))

st.caption("Disclaimer: Educational purposes only.")
