# End-to-End Implementation Plan & Architecture: A/B Testing & Uplift Modeling System

## 1. Project Objective (Restated)
The objective is to transform an existing causal inference and uplift modeling prototype—designed to optimize marketing campaign targeting by identifying "Persuadables"—into a fully functional, deploy-ready, and scalable solution. This involves bridging statistical modeling with robust software engineering, scalable architecture, and actionable business insights.

## 2. Key Components of the Plan

### Phase 1: Foundation & Project Setup (Weeks 1-2)
*   **Deliverables:** Dockerized environment, CI/CD pipeline (GitHub Actions), initialized test suite (`pytest`).
*   **Dependencies:** Access to a sample dataset (`hillstrom_email_campaign.csv`) and clear definitions of input data schemas.

### Phase 2: Core Engineering & Backend Modularization (Weeks 3-4)
*   **Deliverables:** Refactored `src/` directory with object-oriented ML predictors and statistical utilities, robust error logging, and data validation (using Great Expectations or Pandera).
*   **Dependencies:** Completion of Phase 1; stable model artifacts (`models/xlearner_model.pkl`).

### Phase 3: Frontend Dashboard Refinement (Week 5)
*   **Deliverables:** Enhanced Streamlit application (`app/streamlit_app.py`) featuring cached inference, interactive Qini curves, decile analysis, and business impact summaries.
*   **Dependencies:** Stable backend interfaces from Phase 2.

### Phase 4: Testing, UAT & Deployment (Week 6)
*   **Deliverables:** Comprehensive test coverage (unit, integration), UAT sign-off from business stakeholders, and production deployment on a containerized service (e.g., Render, AWS ECS).
*   **Dependencies:** Production environment provisioning; successful pipeline runs.

## 3. High-Level Architectural Approach

**Major Modules & Interactions:**
*   **Data Ingestion & Validation Layer:** Processes raw campaign data, ensures schema compliance, and prepares features.
*   **Inference Engine (`src/` & `models/`):** Loads pre-trained causal models (e.g., X-Learner). Exposes an interface to score incoming user batches, returning uplift deciles.
*   **Presentation Layer (`app/`):** A Streamlit-based web application that queries the Inference Engine, aggregates the results, and displays interactive marketing KPIs.

**Technology Considerations:**
*   **Backend:** Python 3.10+, Pandas, CausalML, EconML, Scikit-learn.
*   **Frontend:** Streamlit, Plotly for visualizations.
*   **Infrastructure:** Docker, GitHub Actions. (Future decoupling could introduce FastAPI as an independent REST API layer between the frontend and the models.)

**Scalability & Security Implications:**
*   **Scalability:** The monolithic Streamlit approach is sufficient for a few concurrent users. For high concurrency, the Inference Engine must be extracted into a standalone API (e.g., FastAPI) deployed across a load-balanced cluster. Model artifacts should be served from cloud storage rather than bundled directly.
*   **Security:** Since this deals with customer data, the system requires strict network security (VPC), access controls (IAM), and data anonymization before ingestion. No PII should be logged.

## 4. Critical Risks, Assumptions, & Mitigation

*   **Assumption 1:** The provided data schema matches the model's expected features exactly.
    *   *Mitigation:* Implement strict data contracts and validation at the ingestion layer before passing data to the models.
*   **Risk 1: Model Drift & Degradation.** Customer behavior changes over time, meaning the Uplift model will lose effectiveness.
    *   *Mitigation:* Establish a feedback loop. Continuously run a random holdout control group (10% of campaigns) to monitor real vs. predicted uplift. Set up automated model retraining triggers.
*   **Risk 2: Performance Bottlenecks.** In-memory scoring of large datasets within Streamlit can lead to out-of-memory errors.
    *   *Mitigation:* Use batch processing for scoring large lists offline, saving results to a database. Streamlit should query the pre-calculated database rather than inferring in real-time.

## 5. Clarifying Questions

1.  **Data Source Integration:** Will the production system need to pull data dynamically from a data warehouse (e.g., Snowflake, BigQuery), or will users manually upload CSV files?
2.  **User Authentication:** Does the Streamlit dashboard require integration with a Single Sign-On (SSO) provider (e.g., Okta, Azure AD) for internal team access?
3.  **Model Retraining Frequency:** How often does the marketing team expect the underlying X-Learner model to be retrained with new campaign data?

## 6. Next Concrete Steps

1.  **Align on Architecture:** Review this high-level design and answer the clarifying questions to lock in the final architecture.
2.  **Initialize Environments:** Set up the Git repository with the proposed directory structure, create the `Dockerfile`, and configure GitHub Actions for CI.
3.  **Data Contract Definition:** Document the exact input schema expected by the `xlearner_model.pkl` to inform data engineering tasks.
