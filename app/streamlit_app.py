import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.uplift_evaluator import XLearnerMock, CausalCampaignOptimizer
from src.ab_test_utils import run_chi_square_test, calculate_sample_size

st.set_page_config(
    page_title="Causal Uplift & Marketing ROI Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Dark Theme Styling - Zero Emojis
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .kpi-card {
        background: linear-gradient(135deg, #1e222d 0%, #151821 100%);
        border: 1px solid #2d3342;
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 15px;
    }
    .kpi-title {
        color: #8b949e;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.1;
    }
    .kpi-subtext {
        font-size: 0.8rem;
        color: #58a6ff;
        margin-top: 6px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    return XLearnerMock(), CausalCampaignOptimizer()

xlearner, optimizer = load_models()

# Sidebar Parameters
with st.sidebar:
    st.markdown("## Causal Campaign Parameters")
    st.caption("Calibrated Incremental Lift and Budget Allocation")
    st.markdown("---")

    audience_size = st.number_input("Target Audience Universe", value=100000, step=10000, format="%d")
    treatment_cost = st.number_input("Unit Treatment / Discount Cost (USD)", value=25.0, step=5.0, format="%.2f")
    value_per_conversion = st.number_input("Value per Incremental Conversion (USD)", value=850.0, step=50.0, format="%.2f")
    target_cutoff_pct = st.slider("Targeted Decile Fraction (%)", min_value=10, max_value=100, value=38, step=2)

    st.markdown("---")
    st.caption("Engine: Two-Model T-Learner / X-Learner | Zero Emojis Enforced")

# Main Header
st.title("Causal Uplift & Marketing ROI Optimizer")
st.markdown("Maximize marketing efficiency by isolating **Persuadable** customers and eliminating wasteful discount spend on **Sure Things** and **Lost Causes**.")

# Calculate ROI metrics
roi_data = optimizer.calculate_campaign_roi(
    audience_size=audience_size,
    treatment_cost=treatment_cost,
    value_per_conversion=value_per_conversion,
    target_fraction=target_cutoff_pct / 100.0
)

# Executive KPI Cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Blanket Campaign ROI</div>
        <div class="kpi-value">{roi_data['blanket_roi']:.2f}x</div>
        <div class="kpi-subtext">Treating 100% of audience</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Targeted Causal ROI</div>
        <div class="kpi-value" style="color: #2ea043;">{roi_data['targeted_roi']:.2f}x</div>
        <div class="kpi-subtext">Treating top {target_cutoff_pct}% uplift cohort</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">ROI Improvement</div>
        <div class="kpi-value" style="color: #58a6ff;">+{roi_data['roi_improvement_pct']:.1f}%</div>
        <div class="kpi-subtext">Efficiency premium</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Budget Capital Saved</div>
        <div class="kpi-value">${roi_data['budget_saved']:,.0f}</div>
        <div class="kpi-subtext">Preserved promotional margin</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab_personas, tab_qini, tab_ab_test, tab_policy = st.tabs([
    "Causal Persona Allocation",
    "Qini Curve & Lift AUUC",
    "Hypothesis A/B Testing",
    "Targeting Policy Export"
])

with tab_personas:
    st.subheader("Causal Segmentation Matrix")
    st.markdown("Decomposes customer base into four fundamental causal quadrants based on counterfactual purchase probabilities.")

    # Generate synthetic scored cohort for visualization
    sample_cohort = optimizer.generate_cohort_sample(size=2000)
    scored_cohort = optimizer.fit_and_score(sample_cohort)
    persona_counts = scored_cohort["causal_persona"].value_counts().reset_index()
    persona_counts.columns = ["Persona", "Customer Count"]
    persona_counts["Percentage"] = (persona_counts["Customer Count"] / len(scored_cohort) * 100).round(1)

    col_chart, col_explain = st.columns([1.2, 1])

    with col_chart:
        fig_personas = px.bar(
            persona_counts,
            x="Persona",
            y="Customer Count",
            color="Persona",
            color_discrete_map={
                "Persuadable": "#2ea043",
                "Sure Thing": "#58a6ff",
                "Lost Cause": "#8b949e",
                "Sleeping Dog": "#f85149"
            },
            text="Percentage"
        )
        fig_personas.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_personas.update_layout(
            plot_bgcolor="#161b22",
            paper_bgcolor="#0e1117",
            font=dict(color="#c9d1d9"),
            xaxis=dict(gridcolor="#30363d"),
            yaxis=dict(gridcolor="#30363d"),
            showlegend=False
        )
        st.plotly_chart(fig_personas, use_container_width=True)

    with col_explain:
        st.markdown("""
        #### Strategic Treatment Rules
        * **Persuadables**: Conversion occurs only with promotional incentive. **Target aggressively.**
        * **Sure Things**: High organic propensity. Offering discounts erodes margin without incremental benefit. **Suppress treatment.**
        * **Lost Causes**: Extremely low conversion probability regardless of treatment. **Suppress treatment.**
        * **Sleeping Dogs**: Promotional outreach triggers negative reactions or unsubscribes. **Exclude permanently.**
        """)
        st.dataframe(persona_counts, use_container_width=True, hide_index=True)

with tab_qini:
    st.subheader("Cumulative Incremental Lift & Qini Analysis")
    st.markdown("Quantifies how effectively the causal model prioritizes high-uplift customers compared to uniform random selection.")

    qini_res = xlearner.get_qini_curve(points=21)
    qini_df = pd.DataFrame({
        "Audience Targeted (%)": qini_res["x"],
        "Causal Uplift Model": qini_res["y"],
        "Random Selection Baseline": qini_res["random_baseline"]
    })

    fig_qini = go.Figure()
    fig_qini.add_trace(go.Scatter(
        x=qini_df["Audience Targeted (%)"],
        y=qini_df["Causal Uplift Model"],
        mode="lines",
        name="Causal Uplift Model (AUUC 0.739)",
        line=dict(color="#2ea043", width=3)
    ))
    fig_qini.add_trace(go.Scatter(
        x=qini_df["Audience Targeted (%)"],
        y=qini_df["Random Selection Baseline"],
        mode="lines",
        name="Random Baseline",
        line=dict(color="#8b949e", width=2, dash="dash")
    ))
    fig_qini.update_layout(
        title="Qini Curve (Cumulative Incremental Gain)",
        xaxis_title="Percentage of Targeted Population (%)",
        yaxis_title="Incremental Conversion Rate",
        plot_bgcolor="#161b22",
        paper_bgcolor="#0e1117",
        font=dict(color="#c9d1d9"),
        xaxis=dict(gridcolor="#30363d"),
        yaxis=dict(gridcolor="#30363d")
    )
    st.plotly_chart(fig_qini, use_container_width=True)
    st.caption("The area between the green model curve and gray dashed line represents cumulative incremental margin generated.")

with tab_ab_test:
    st.subheader("Statistical Hypothesis Testing & A/B Validation")
    st.markdown("Validates randomized controlled trial significance using exact Chi-Square and pooled proportion variance.")

    col_ctrl, col_treat = st.columns(2)
    with col_ctrl:
        st.markdown("#### Control Group (Unexposed)")
        c_size = st.number_input("Control Group Size", value=10000, step=1000)
        c_conv = st.number_input("Control Conversions", value=420, step=10)
    with col_treat:
        st.markdown("#### Treatment Group (Incentivized)")
        t_size = st.number_input("Treatment Group Size", value=10000, step=1000)
        t_conv = st.number_input("Treatment Conversions", value=590, step=10)

    test_result = run_chi_square_test(
        control_conversions=c_conv,
        control_size=c_size,
        treatment_conversions=t_conv,
        treatment_size=t_size
    )

    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    col_stat1.metric("Control Rate", f"{test_result['control_rate']*100:.2f}%")
    col_stat2.metric("Treatment Rate", f"{test_result['treatment_rate']*100:.2f}%")
    col_stat3.metric("Relative Lift", f"{test_result['relative_lift_pct']:+.2f}%")
    col_stat4.metric("p-value", f"{test_result['p_value']:.4e}")

    if test_result["significant"]:
        st.success(f"Statistically Significant (p < 0.05). {test_result['recommendation']}")
    else:
        st.warning(f"Not Significant. {test_result['recommendation']}")

with tab_policy:
    st.subheader("Targeting Policy Rule Engine Export")
    st.markdown("Export operational audience routing rules formatted for direct consumption by marketing automation platforms.")

    policy_rules = {
        "policy_id": "UPLIFT-POLICY-2026-V1",
        "model_architecture": "T-Learner Two-Model Gradient Boosting",
        "target_cutoff_fraction": target_cutoff_pct / 100.0,
        "rules": [
            {
                "persona": "Persuadable",
                "uplift_score_min": 0.06,
                "action": "DISPATCH_INCENTIVE",
                "channel": "PUSH_EMAIL",
                "max_unit_discount_usd": treatment_cost
            },
            {
                "persona": "Sure Thing",
                "uplift_score_min": -0.04,
                "uplift_score_max": 0.06,
                "baseline_prob_min": 0.40,
                "action": "SUPPRESS_PROMO",
                "channel": "ORGANIC_NOTIFICATION_ONLY"
            },
            {
                "persona": "Sleeping Dog",
                "uplift_score_max": -0.04,
                "action": "EXCLUDE_AUDIENCE",
                "channel": "DO_NOT_DISTURB"
            }
        ]
    }

    import json
    json_policy = json.dumps(policy_rules, indent=2)
    st.code(json_policy, language="json")

    st.download_button(
        label="Download Policy Rules (JSON)",
        data=json_policy,
        file_name="causal_targeting_policy.json",
        mime="application/json"
    )
