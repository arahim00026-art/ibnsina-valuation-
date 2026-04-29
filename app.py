import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="Ibn Sina Pharma | Strategic Financial Forecast",
    page_icon="💊",
    layout="wide"
)

# Custom CSS for a professional corporate look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 8px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #003366;
    }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE FINANCIAL ENGINE ---
@st.cache_data
def calculate_forecast(growth_rate):
    # 2025 Base Year Values (Extracted from Standalone Financial Statements)[cite: 1]
    base_year = 2025
    ebit_2025 = 3568567510
    tax_rate = 0.114 # Current Tax (248.3M) / Net Profit before Tax (1,039.2M)[cite: 1]
    depreciation = 323549823
    capex = 702174074
    delta_wc = 1121873988
    
    # Base FCFF Calculation for 2025
    base_fcff = (ebit_2025 * (1 - tax_rate)) + depreciation - capex - delta_wc
    
    # Projection Years: 2026 to 2030
    years = np.arange(2026, 2031)
    
    # Generate Forecast Data
    ebit_f = [ebit_2025 * (1 + growth_rate)**(i+1) for i in range(len(years))]
    fcff_f = [base_fcff * (1 + growth_rate)**(i+1) for i in range(len(years))]
    
    return pd.DataFrame({
        "Year": years,
        "Projected_EBIT": ebit_f,
        "Projected_FCFF": fcff_f
    })

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.image("https://ibnsina-pharma.com/wp-content/uploads/2019/08/logo.png", width=200)
st.sidebar.title("Forecast Controls")
growth_input = st.sidebar.slider("Annual Growth Rate (%)", 0, 30, 12) / 100
wacc_input = st.sidebar.number_input("WACC (%)", value=15.0) / 100

st.sidebar.markdown("---")
st.sidebar.write("**Dashboard Prepared by:**")
st.sidebar.info("Abdelrahim Elsweedy")

# --- 4. DASHBOARD HEADER ---
st.title("📈 Ibn Sina Pharma: 5-Year Strategic Valuation Dashboard")
st.markdown("### Focus Period: 2026 – 2030")

# --- 5. EXECUTIVE SUMMARY METRICS ---
df = calculate_forecast(growth_input)
avg_fcff = df["Projected_FCFF"].mean()
total_fcff = df["Projected_FCFF"].sum()
terminal_growth = 0.03
terminal_value = (df["Projected_FCFF"].iloc[-1] * (1 + terminal_growth)) / (wacc_input - terminal_growth)

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Avg. Projected FCFF (26-30)", f"EGP {avg_fcff/1e9:.2f} B")
with m2:
    st.metric("Cumulative 5-Year Cash Flow", f"EGP {total_fcff/1e9:.2f} B")
with m3:
    st.metric("Estimated Terminal Value", f"EGP {terminal_value/1e9:.2f} B")

st.markdown("---")

# --- 6. VISUAL ANALYTICS ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("FCFF vs EBIT Projection Trajectory")
    fig = go.Figure()
    
    # FCFF Bars
    fig.add_trace(go.Bar(
        x=df["Year"], y=df["Projected_FCFF"],
        name="Projected FCFF", marker_color='#003366'
    ))
    
    # EBIT Line
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["Projected_EBIT"],
        name="Projected EBIT", line=dict(color='#ff9900', width=4)
    ))

    fig.update_layout(
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_title="EGP (Amount in Billions)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Forecast Data Summary")
    display_df = df.copy()
    display_df["Projected_EBIT"] = (display_df["Projected_EBIT"] / 1e6).map('{:,.1f}M'.format)
    display_df["Projected_FCFF"] = (display_df["Projected_FCFF"] / 1e6).map('{:,.1f}M'.format)
    st.dataframe(display_df, height=300, use_container_width=True)

# --- 7. FINAL DISCLAIMER & FOOTER ---
st.markdown("---")
st.subheader("Financial Notes & Methodology")
st.write("""
This dashboard utilizes the **Free Cash Flow to the Firm (FCFF)** model. 
The 2025 base values are derived directly from the Standalone Financial Statements[cite: 1]:
- **Operating Profit (EBIT):** EGP 3.57 Billion[cite: 1]
- **Effective Tax Rate:** 11.4%[cite: 1]
- **Significant Drivers:** The forecast accounts for the EGP 702M CapEx and EGP 1.12B Working Capital requirements recorded in 2025[cite: 1].
""")

st.warning("""
**Disclaimer:** This dashboard is for educational and analytical purposes only. 
The projections are based on mathematical growth assumptions and do not constitute 
financial advice or a guarantee of future stock performance.
""")

st.markdown(
    "<div style='text-align: center; color: grey; padding: 20px;'>"
    "Prepared by Abdelrahim Elsweedy, FMVA "
    "</div>", 
    unsafe_allow_html=True
)
