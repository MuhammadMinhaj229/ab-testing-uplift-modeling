import pandas as pd
import numpy as np

class XLearnerMock:
    def __init__(self):
        self.auuc = 0.739
    def predict_uplift(self, df):
        # Simulate an uplift score for each row based on random noise centered around a mean
        return np.random.normal(loc=0.05, scale=0.1, size=len(df))
    def get_qini_curve(self):
        # Return a mock Qini curve matching the AUUC score
        return {"x": np.linspace(0, 100, 10), "y": np.linspace(0, 0.168, 10)}
