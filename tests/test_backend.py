import pytest
from src.uplift_evaluator import XLearnerMock
from src.ab_test_utils import run_chi_square_test
import pandas as pd

def test_xlearner_mock():
    model = XLearnerMock()
    df = pd.DataFrame({'id': [1,2,3]})
    assert len(model.predict_uplift(df)) == 3

def test_ab_test():
    res = run_chi_square_test(100, 1000, 150, 1000)
    assert res['significant'] == True
