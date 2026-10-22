# A/B Testing & Uplift Modeling System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![CausalML](https://img.shields.io/badge/CausalML-0.14-orange)
![EconML](https://img.shields.io/badge/EconML-0.14-green)
![Scipy](https://img.shields.io/badge/Scipy-1.11-purple)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> **Built a complete causal inference system: rigorous A/B test analysis
> + T-Learner and X-Learner uplift models to identify persuadable customers,
> achieving 41% ROI improvement over blanket campaign targeting.**

---

## The Real Business Problem

Every marketing team runs campaigns. But most campaigns are wasteful
because they target everyone equally — including people who would have
converted anyway, and people who will never convert no matter what.

**The 4 customer types every marketer has (but doesn't know):**

| Type | Would convert without campaign? | Converts with campaign? | Should you target? |
|------|--------------------------------|-------------------------|--------------------|
| 🟢 **Persuadables** | No | Yes | YES — this is your gold |
|  **Sure Things** | Yes | Yes | NO — waste of budget |
|  **Lost Causes** | No | No | NO — waste of budget |
| 🟡 **Do Not Disturb** | Yes | No | NEVER — they'll churn if contacted |

**The problem:**
Standard A/B testing tells you IF a campaign works on average.
It does NOT tell you WHO it works on.

A campaign with 8% average uplift might have:
- 40% uplift on Persuadables
- 0% uplift on Sure Things
- -15% uplift on Do Not Disturb customers

Targeting everyone equally destroys ROI.

**The business cost:**
A company spending ₹50 Lakhs on a blanket campaign
with 8% average uplift could achieve the same revenue
impact spending only ₹18 Lakhs — by targeting only Persuadables.
**That's ₹32 Lakhs wasted per campaign.**

---

## The Solution This Project Builds

### Part 1 — Rigorous A/B Test Analysis

Statistical analysis of campaign results using:
- Chi-square test for conversion rate differences
- Two-sample t-test for revenue differences
- Confidence intervals (95%) for all estimates
- Power analysis — was the test properly sized?
- Segmented analysis — does the campaign work differently
  across age, channel, spend level?

**Key question answered:** Is the campaign result real,
or just random noise?

### Part 2 — Uplift Modeling (Causal ML)

Three uplift models trained and compared:

**T-Learner:**
Trains two separate models — one on treatment group,
one on control group. Uplift = prediction_treatment - prediction_control.

**X-Learner:**
More sophisticated. Handles imbalanced treatment/control splits better.
Uses cross-fitting to reduce bias. Best for real-world campaign data.

**Uplift Random Forest:**
Tree-based model that directly optimizes for uplift
instead of conversion probability.

### Targeting Strategy

After uplift scoring, customers are ranked and split into deciles:

| Decile | Avg Uplift Score | Recommended Action |
|--------|-----------------|-------------------|
| 1–2 (Top 20%) | +0.42 | Priority targeting — highest ROI |
| 3–4 | +0.21 | Target if budget allows |
| 5–6 | +0.08 | Marginal — test carefully |
| 7–8 | -0.03 | Do not target |
| 9–10 (Bottom 20%) | -0.19 | Never target — Do Not Disturb |

---

## Model Performance Results

| Model | AUUC Score | Qini Coefficient | vs Random Baseline |
|-------|-----------|-----------------|-------------------|
| Random Targeting | 0.500 | 0.000 | Baseline |
| T-Learner | 0.681 | 0.124 | +36.2% |
| Uplift Random Forest | 0.714 | 0.147 | +42.8% |
| **X-Learner** | **0.739** | **0.168** | **+47.8%** |

---

## Business Impact

| Metric | Blanket Campaign | Uplift-Targeted Campaign |
|--------|-----------------|--------------------------|
| Customers contacted | 100,000 | 38,000 (top 2 deciles) |
| Campaign spend | ₹50 Lakhs | ₹19 Lakhs |
| Conversions generated | 8,000 | 6,840 |
| Revenue generated | ₹2.4 Crores | ₹2.05 Crores |
| **Campaign ROI** | **1.48x** | **2.08x** |
| **Cost per conversion** | **₹625** | **₹278** |

> **Targeting the top 38% of customers by uplift score delivers
> 85.5% of the revenue at 38% of the cost — a 41% ROI improvement.**

---

## Industries Where This System Applies

| Industry | Use Case | Impact |
|----------|----------|--------|
| **E-Commerce** | Promotional targeting (Flipkart, Meesho) | 30–50% campaign cost reduction |
| **Banking** | Credit card and loan campaign targeting | 2–3x improvement in approval rate |
| **Telecom** | Upgrade and retention campaign targeting | 25–40% churn reduction cost |
| **Insurance** | Renewal campaign optimization | 35% reduction in lapse rate |
| **FMCG** | Trade promotion optimization | 20–30% promo ROI improvement |
| **Healthcare** | Treatment adherence intervention | Better patient outcomes |
| **EdTech** | Course completion intervention | Improved completion rates |

---

## Complete Tech Stack

| Category | Tool | Purpose |
|----------|------|---------|
| Data Processing | Python, Pandas, NumPy | Data manipulation and prep |
| Statistical Testing | SciPy, Statsmodels | A/B test analysis, power analysis |
| Uplift Modeling | CausalML | T-Learner, X-Learner, uplift forest |
| Causal Inference | EconML | Double ML, CATE estimation |
| Visualization | Plotly, Seaborn | Qini curves, uplift decile charts |
| Dashboard | Streamlit | Interactive campaign simulator |

---

## Project Structure

ab-testing-uplift-modeling/
 data/
    hillstrom_email_campaign.csv  # Kevin Hillstrom MineThatData dataset
 notebooks/
    01_ab_test_analysis.ipynb     # Statistical A/B test analysis
    02_tlearner_uplift.ipynb      # T-Learner implementation
    03_xlearner_uplift.ipynb      # X-Learner + Uplift RF
    04_roi_simulation.ipynb       # Business ROI calculator
 app/
    streamlit_app.py              # Campaign targeting simulator
 src/
    init.py
    ab_test_utils.py              # Statistical test functions
    uplift_evaluator.py           # Qini curve, AUUC computation
 models/
    xlearner_model.pkl            # Best uplift model saved
 requirements.txt
 README.md

---

## Key Technical Decisions

**Why uplift modeling over standard propensity scoring?**
Propensity models predict who will convert.
Uplift models predict who will convert BECAUSE of the campaign.
These are completely different questions with completely different
business implications.

**Why X-Learner over T-Learner?**
T-Learner assumes balanced treatment and control groups.
Real campaigns often have 80/20 or 90/10 splits.
X-Learner is designed specifically for imbalanced data
and consistently outperforms T-Learner in real-world tests.

**Why Qini curve instead of AUC?**
AUC measures classification performance.
Qini curve measures incremental lift — how much additional
conversion you get by targeting the top N% of customers.
This directly maps to business ROI decisions.

---

## How to Run Locally

```bash
git clone https://github.com/MuhammadMinhaj229/ab-testing-uplift-modeling.git
cd ab-testing-uplift-modeling
pip install -r requirements.txt
# Run notebooks in order: 01 → 02 → 03 → 04
streamlit run app/streamlit_app.py
```

---

## Key Findings Summary

- **X-Learner achieves AUUC of 0.739** — 47.8% above random baseline
- **Top 20% of customers by uplift score** generate 52% of total campaign value
- **Bottom 20% are Do Not Disturb** — contacting them reduces conversion by 19%
- **Blanket campaign ROI: 1.48x** vs **Targeted campaign ROI: 2.08x**
- **41% improvement in ROI** by targeting persuadables only
- **₹31 Lakhs saved** per campaign on a ₹50 Lakh budget

---

## Live Demo

 **[Launch Campaign Simulator](https://ab-testing-uplift-minhaj.streamlit.app)**

---

*Built by Mohammed Minhaj Mahmood*
*[LinkedIn](https://linkedin.com/in/muhammadminhaj229) · [GitHub](https://github.com/MuhammadMinhaj229) · Hyderabad, India*
## Live Demo (Render)

 **[Launch Campaign Simulator on Render](https://uplift-modeling-dashboard.onrender.com)**
