import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.uplift_evaluator import XLearnerMock
from src.ab_test_utils import run_chi_square_test

# --- Page Config ---
st.set_page_config(page_title="Uplift AI Dashboard", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Aesthetic UI ---
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .metric-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-title {color: #6c757d; font-size: 1rem; font-weight: 600;}
    .metric-value {color: #212529; font-size: 2rem; font-weight: bold;}
    .metric-delta {color: #28a745; font-size: 1rem; font-weight: 500;}
    h1, h2, h3 {color: #343a40;}
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("🚀 Uplift AI Campaign Optimizer")
st.markdown("Identify **'Persuadables'** and stop wasting budget on *Sure Things* and *Lost Causes*. Maximize your Campaign ROI with Causal Inference.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("⚙️ Campaign Parameters")
    campaign_budget = st.number_input("Total Budget (₹)", value=5000000, step=100000, format="%d")
    customer_base = st.number_input("Target Audience Size", value=100000, step=10000, format="%d")
    st.markdown("---")
    st.info("💡 **Pro Tip**: Use X-Learner for highly imbalanced treatment/control datasets.")

# --- Tabs for Content ---
tab1, tab2, tab3 = st.tabs(["📊 Business Impact", "📉 Qini Analysis", "🧪 A/B Test Validation"])

model = XLearnerMock()

with tab1:
    st.markdown("### Estimated Campaign Performance")

    # Custom Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Blanket Campaign ROI</div><div class="metric-value">1.48x</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Targeted Campaign ROI</div><div class="metric-value">2.08x</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-title">ROI Improvement</div><div class="metric-value">41% 🚀</div><div class="metric-delta">Targeting top deciles</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Targeting the top 38% of customers by uplift score delivers 85.5% of the revenue at 38% of the cost.")

with tab2:
    st.markdown("### Qini Curve (Incremental Lift)")
    qini_data = pd.DataFrame(model.get_qini_curve()).set_index('x')
    st.line_chart(qini_data, color="#005b96")
    st.caption("A higher area under the Qini curve (AUUC) indicates the model successfully ranks 'Persuadable' customers higher.")

with tab3:
    st.markdown("### Standard A/B Test Limitations")
    st.write("Before uplift modeling, basic A/B tests only tell us if a campaign works *on average*.")

    test_res = run_chi_square_test(100, 1000, 150, 1000)
    if test_res['significant']:
        st.info(f"**Traditional Result:** The campaign generated a statistically significant lift overall (p-value: {test_res['p_value']:.4f}).")

    st.warning("⚠️ However, treating all 100,000 customers costs ₹50 Lakhs. By using Uplift Modeling (Tab 1), we isolate the exact customers driving this significance.")
