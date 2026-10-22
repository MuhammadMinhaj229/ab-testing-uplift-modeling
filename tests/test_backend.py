import pytest
import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.uplift_evaluator import XLearnerMock, CausalCampaignOptimizer
from src.ab_test_utils import run_chi_square_test, calculate_sample_size

def test_xlearner_mock():
    model = XLearnerMock()
    df = pd.DataFrame({'id': [1, 2, 3]})
    scores = model.predict_uplift(df)
    assert len(scores) == 3
    qini = model.get_qini_curve()
    assert "x" in qini
    assert "y" in qini
    assert len(qini["x"]) == len(qini["y"])

def test_ab_test():
    res = run_chi_square_test(100, 1000, 150, 1000)
    assert res['significant'] is True
    assert res['p_value'] < 0.05
    assert 'relative_lift_pct' in res

def test_causal_optimizer():
    optimizer = CausalCampaignOptimizer()
    cohort = optimizer.generate_cohort_sample(size=200)
    assert len(cohort) == 200
    assert "treatment" in cohort.columns
    assert "converted" in cohort.columns
    
    scored = optimizer.fit_and_score(cohort)
    assert "uplift_score" in scored.columns
    assert "causal_persona" in scored.columns
    personas = set(scored["causal_persona"].unique())
    assert len(personas) >= 2

def test_campaign_roi_calculator():
    optimizer = CausalCampaignOptimizer()
    roi_data = optimizer.calculate_campaign_roi(
        audience_size=100000,
        treatment_cost=50,
        value_per_conversion=1500,
        target_fraction=0.38
    )
    assert roi_data["targeted_roi"] > roi_data["blanket_roi"]
    assert roi_data["budget_saved"] > 0
