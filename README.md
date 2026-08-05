# Uplift Modeling Dashboard Simulation

A mocked Streamlit dashboard demonstrating the user interface and theoretical business impact of uplift modeling for marketing campaigns.

## Problem / Motivation

Marketing campaigns often target all users indiscriminately. Uplift modeling seeks to answer not just who will convert, but who will convert *because* of the campaign. The goal is to identify "persuadable" customers to target while avoiding those who would buy anyway, those who won't buy regardless, and those who react negatively to marketing. This repository provides a simulated front-end dashboard to explore how these metrics (like AUUC, Qini curves, and incremental ROI) could be presented to stakeholders.

## Approach

The current codebase implements a front-end simulation using Streamlit.
- **Frontend**: A dashboard containing three tabs: Estimated Campaign Performance, Qini Analysis, and A/B Test Validation.
- **Backend**: A mocked backend environment. The `XLearnerMock` class provides hardcoded and randomized outputs designed to simulate uplift predictions. The `run_chi_square_test` function returns static statistical significance values.

## Results

*No real models are trained and no datasets are processed in this repository.* All displayed results in the dashboard are mocked for UI demonstration purposes.
- The AUUC and Qini curve metrics are simulated (see `src/uplift_evaluator.py`, `XLearnerMock`).
- A/B test results are hardcoded (see `src/ab_test_utils.py`, `run_chi_square_test`).

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- SciPy
- Pytest

## Project Structure

```
.
├── app/
│   └── streamlit_app.py
├── models/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── ab_test_utils.py
│   └── uplift_evaluator.py
├── tests/
│   └── test_backend.py
├── Dockerfile
├── IMPLEMENTATION_PLAN.md
├── render.yaml
├── requirements.txt
└── README.md
```

## How to Run Locally

1. Clone the repository and navigate into the directory.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app/streamlit_app.py
   ```
4. Run the test suite:
   ```bash
   python -m pytest
   ```

## Limitations & Future Work

- **Fully Mocked Implementation**: The current codebase does not include real datasets, data processing pipelines, or actual Causal ML models. All outputs are currently hardcoded or randomized.
- **Future Integration**: Real causal inference models (using libraries like CausalML or EconML) need to be implemented to replace `XLearnerMock`.
- **Data Integration**: Actual campaign data (e.g., A/B test logs) needs to be piped into the backend for real analysis rather than relying on static placeholders.

## Author / Links

*Built by Mohammed Minhaj Mahmood*
*[LinkedIn](https://linkedin.com/in/muhammadminhaj229) · [GitHub](https://github.com/MuhammadMinhaj229) · Hyderabad, India*

👉 **[Launch Campaign Simulator on Render](https://uplift-modeling-dashboard.onrender.com)**
