# End-to-End Implementation Plan: A/B Testing & Uplift Modeling System

This document outlines the end-to-end plan to transform the existing A/B Testing & Uplift Modeling prototype into a fully functional, deploy-ready, and scalable solution. This plan integrates perspectives from software engineering, business analysis, and data analytics.

## 1. System Architecture & Technology Stack

**Architecture Overview:**
The system is built as a monolithic modular application for simplicity and maintainability, composed of a data processing layer, an ML/causal inference backend, and an interactive frontend dashboard.

**Technology Stack Recommendations:**
*   **Frontend:** Streamlit (existing) for rapid dashboard development and interactive visualizations, integrated with Plotly.
*   **Backend & Data Processing:** Python 3.10+ (existing). Pandas and NumPy for robust in-memory data transformations.
*   **Machine Learning/Causal Inference:** CausalML (existing), EconML (existing), Scikit-Learn (existing).
*   **API/Service Layer (Future state for scalability):** FastAPI to decouple the frontend from the ML model serving if needed later.
*   **Testing:** `pytest` for unit/integration tests, `Great Expectations` for data validation.
*   **Deployment:** Docker for containerization, deployed on a platform like Render, AWS ECS, or Google Cloud Run.
*   **CI/CD:** GitHub Actions for automated testing, linting, and deployment.

**Component Integration:**
1.  **`src/`:** Contains the core business logic, statistical utility functions (`ab_test_utils.py`), and evaluation metrics (`uplift_evaluator.py`).
2.  **`models/`:** Stores pre-trained ML models (e.g., `xlearner_model.pkl`) to ensure fast inference on the dashboard without retraining on startup.
3.  **`app/`:** Contains the Streamlit frontend application (`streamlit_app.py`) that queries models in `models/` and utilizes logic from `src/`.

*Assumption/Missing Details:* The project currently lacks explicit database integration (e.g., PostgreSQL for storing user simulation runs) and data pipelines (e.g., Airflow). It relies on static CSVs which is fine for prototype but needs a real DB connection for production.

## 2. Step-by-Step Development Roadmap

**Phase 1: Project Setup & Baseline Integrity (Week 1)**
*   **Dev:** Standardize environment (Dockerize the application). Establish `pytest` framework in a new `tests/` directory.
*   **Data:** Define schemas for expected inputs (e.g., campaign data). Setup data validation using Pandera or Great Expectations.
*   **Biz:** Document key KPIs (ROI, Cost per Conversion, Conversion Rate) for tracking.

**Phase 2: Core Engineering & Backend (Week 2-3)**
*   **Dev:** Refactor scripts in `src/` into highly cohesive classes/modules. Implement error handling and logging (using Python's `logging` module).
*   **Data:** Create an automated ETL pipeline script to process new campaign data into the format required by `models/`.
*   **Biz:** Define process flows for how marketing users will interact with the system (inputting data vs. reading outputs).

**Phase 3: Frontend Enhancement & Integration (Week 4)**
*   **Dev:** Enhance `app/streamlit_app.py` for better UX. Add caching (`@st.cache_data`) for performance.
*   **Data:** Build out interactive decile analysis and Qini curve visualizations within the Streamlit app.
*   **Biz:** Review dashboard usability with stakeholders. Ensure the narrative clearly distinguishes "Persuadables" from "Lost Causes".

**Phase 4: Testing & Deployment (Week 5)**
*   **Dev:** Finalize CI/CD pipeline (GitHub Actions). Deploy application to staging.
*   **Data:** Run end-to-end data pipeline tests to verify model predictions match expected distributions.
*   **Biz:** Conduct User Acceptance Testing (UAT). Go-live decision.

## 3. Code Organization Guidelines

*   **`src/`:** Must contain pure Python modules. Avoid running scripts directly here. Functions should be typed using Python `typing` and documented with Google-style docstrings.
*   **`app/`:** Keep Streamlit UI components separate from business logic. UI scripts should import processors from `src/`.
*   **`models/`:** Only contain serialized model artifacts (like `.pkl` or `.onnx`). Include a metadata file detailing model version, training date, and performance metrics.
*   **Missing Directories:** Create `tests/` for all `pytest` cases. Create `notebooks/` strictly for exploratory analysis (not production code). Create `data/` for sample datasets (added to `.gitignore` if sensitive).

## 4. Testing Strategy

*   **Unit Testing:** `pytest` for all functions in `src/` (e.g., testing `ab_test_utils.py` against known statistical distributions).
*   **Integration Testing:** Test the interaction between `app/streamlit_app.py` and the loaded models in `models/`.
*   **Data Testing:** Verify input data shapes, lack of nulls, and expected types before feeding into the uplift models.
*   **Deployment Validations:** Post-deployment smoke tests to ensure the Streamlit endpoint is accessible and returning a 200 OK status.

## 5. Deployment Plan

*   **Environment Setup:** Create a `Dockerfile` using `python:3.10-slim`.
*   **CI/CD Pipeline:** Implement GitHub Actions workflow to run `flake8` (linting), `pytest` (testing), and build the Docker image on PRs to `main`.
*   **Hosting:** Deploy as a containerized web service. (e.g., Render Web Service).
*   **Monitoring:** Use basic health checks for the web server. Log application errors to a centralized logging service (like Datadog or AWS CloudWatch).
*   **Rollback Strategy:** Containerized deployments allow instant rollback by deploying the previous Docker image tag if critical errors are detected post-deployment.

## 6. Business Analysis Summary

*   **Stakeholder Needs:** Marketing teams need a tool to identify which customers to target to maximize campaign ROI and minimize wasted spend on "Sure Things" and "Do Not Disturb" groups.
*   **Success Metrics (KPIs):**
    *   Increase in overall Campaign ROI (Target: 40%+ improvement).
    *   Reduction in Cost per Conversion.
    *   System Uptime (99.9%).
*   **Risk Mitigation:**
    *   *Risk:* Model drift over time. *Mitigation:* Implement quarterly model retraining and performance reviews against random holdout groups.
    *   *Risk:* Low user adoption. *Mitigation:* Ensure dashboard clearly translates statistical outputs (Qini curves) into actionable business language (Revenue/ROI).

## 7. Data Analysis Plan

*   **Data Sources:** Historical campaign data (e.g., `hillstrom_email_campaign.csv`), requiring features like customer demographics, past purchase behavior, treatment applied, and conversion outcome.
*   **Transformation (ETL):** Clean categorical variables, handle missing values, and balance datasets. Define treatment and control flags explicitly.
*   **Analytics Methods:**
    *   A/B Test Analysis: Chi-square and T-tests for basic significance.
    *   Uplift Modeling: T-Learner and X-Learner to estimate Conditional Average Treatment Effect (CATE).
*   **Business Alignment:** Output customer lists ranked by Uplift Decile. The top deciles are fed directly to CRM/email marketing tools, ensuring analytical insights directly drive marketing action and budget allocation.
