# Comprehensive Implementation Plan: A/B Testing & Uplift Modeling System

## 1. Project Objective
Transform an existing causal inference and uplift modeling prototype into a deploy-ready, scalable production solution. This system identifies "Persuadables" to optimize marketing campaign targeting and improve ROI.

## 2. System Architecture & Technology Stack
*   **Frontend (Presentation):** Streamlit (existing), Plotly for interactive dashboards.
*   **Backend & Inference Layer:** Python 3.10+, Pandas, CausalML, EconML, Scikit-learn. Models pre-trained and saved in `models/`.
*   **Data Layer:** In-memory pandas processing (currently), transitioning to structured data pipelines (e.g., PostgreSQL + Airflow) for production.
*   **Infrastructure:** Docker, deployed on cloud platforms like Render or AWS ECS. CI/CD via GitHub Actions.

## 3. Role-by-Role Development Roadmap
**Phase 1: Project Setup & Baseline Integrity (Week 1)**
*   *Software Engineer:* Dockerize the application. Initialize `pytest` in `tests/`. Setup GitHub Actions CI pipeline.
*   *Data Analyst:* Define explicit data schemas for expected inputs (demographics, treatment flag, outcome).
*   *Business Analyst:* Document current baseline KPIs (ROI, Cost per Conversion) to measure future success.

**Phase 2: Core Engineering & Backend Modularization (Weeks 2-3)**
*   *Software Engineer:* Refactor utilities in `src/` to create object-oriented ML predictors. Implement `logging` and structured error handling.
*   *Data Analyst:* Build ETL scripts to map raw campaign data into the required format for models in `models/`.
*   *Business Analyst:* Define user journeys for the marketing team interacting with the Streamlit dashboard in `app/`.

**Phase 3: Frontend Dashboard Refinement (Week 4)**
*   *Software Engineer:* Refine the Streamlit application in `app/`, adding `@st.cache_data` to prevent OOM errors and improve performance.
*   *Data Analyst:* Design the interactive Qini curve and Decile Analysis views to ensure statistical accuracy.
*   *Business Analyst:* Conduct usability reviews with marketing to ensure "Uplift Deciles" are actionable.

**Phase 4: Testing, UAT & Deployment (Week 5)**
*   *Software Engineer:* Complete unit/integration tests. Deploy the Docker container to a staging environment.
*   *Data Analyst:* Validate output distributions (ensure predictions map logically to historical uplift).
*   *Business Analyst:* Facilitate User Acceptance Testing (UAT) and secure Go-Live approval.

## 4. Code Organization Guidelines
*   **`src/`:** Pure Python backend logic, statistical utilities, typed and documented with Google-style docstrings.
*   **`app/`:** Streamlit UI components only; logic must be imported from `src/`.
*   **`models/`:** Serialized artifacts (`.pkl`) with accompanying metadata files tracking versions and metrics.
*   **`tests/`:** Comprehensive `pytest` test suite mirroring the `src/` structure.

## 5. Testing Strategy
*   **Unit Testing:** Validate statistical formulas and metric calculations in `src/`.
*   **Integration Testing:** Ensure the Streamlit application in `app/` correctly interfaces with the loaded models in `models/`.
*   **Data Validation:** Use Great Expectations/Pandera in the data pipeline to verify schema constraints before inference.

## 6. Deployment Plan
*   **Environment:** Containerized via Docker using `python:3.10-slim`.
*   **CI/CD:** GitHub Actions workflows triggered on PRs to run `pytest` and build Docker images.
*   **Hosting:** Deploy to a managed container service (e.g., Render Web Service) to ensure scalability.
*   **Monitoring/Rollback:** Basic health checks on port 8501. Rollbacks achieved by reverting to the previous Docker image tag.

## 7. Business Analysis Summary
*   **Stakeholder Needs:** Marketing requires actionable lists of "Persuadable" customers to reduce wasted spend on "Sure Things" and "Lost Causes."
*   **Success Metrics:** +40% Improvement in Campaign ROI, -30% Cost per Conversion, 99.9% Application Uptime.
*   **Risk & Mitigation:**
    *   *Model Drift:* Implement quarterly retraining protocols.
    *   *User Adoption:* Dashboard must translate complex Qini curves into simple business terms (Revenue Impact).

## 8. Data Analysis Plan
*   **Data Sources:** Historical campaign data (e.g., sample CSV data), requiring customer attributes, treatment flags, and conversion results.
*   **Transformation (ETL):** Impute missing values, one-hot encode categorical features, and ensure treatment/control balance.
*   **Analytics Methods:** A/B Test Analysis (T-tests/Chi-square) for baseline significance, followed by CausalML/EconML T-Learner and X-Learner for CATE estimation.
*   **Insights:** Outputting rank-ordered customer lists by Uplift Score deciles, feeding top deciles directly to CRM execution tools.

## 9. Clarifying Questions & Next Steps
*   **Q:** Should we proceed immediately with Phase 1 (Docker/CI/Pytest setup) as the next concrete action?
*   **Action:** Align on this plan and begin executing the Software Engineer tasks in Phase 1.
