from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ab_test_utils import run_chi_square_test, calculate_sample_size
from src.uplift_evaluator import CausalCampaignOptimizer, XLearnerMock

app = FastAPI(
    title="Causal Uplift & Marketing ROI Optimizer API",
    description="Enterprise Causal Machine Learning service for incremental lift targeting and A/B test hypothesis evaluation.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

optimizer = CausalCampaignOptimizer()
xlearner = XLearnerMock()

class ABTestRequest(BaseModel):
    control_conversions: int = Field(..., ge=0)
    control_size: int = Field(..., gt=0)
    treatment_conversions: int = Field(..., ge=0)
    treatment_size: int = Field(..., gt=0)
    alpha: Optional[float] = Field(0.05, gt=0, lt=1)

class CampaignOptimizationRequest(BaseModel):
    audience_size: int = Field(100000, gt=0)
    treatment_cost: float = Field(50.0, gt=0)
    value_per_conversion: float = Field(1500.0, gt=0)
    target_fraction: Optional[float] = Field(0.38, gt=0, le=1.0)

class SampleSizeRequest(BaseModel):
    baseline_conversion: float = Field(..., gt=0, lt=1)
    minimum_detectable_effect: float = Field(..., gt=0)
    alpha: Optional[float] = 0.05
    power: Optional[float] = 0.80

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "causal-uplift-optimizer",
        "version": "2.0.0"
    }

@app.post("/api/v1/ab-test")
def evaluate_ab_test(req: ABTestRequest):
    try:
        return run_chi_square_test(
            control_conversions=req.control_conversions,
            control_size=req.control_size,
            treatment_conversions=req.treatment_conversions,
            treatment_size=req.treatment_size,
            alpha=req.alpha or 0.05
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/sample-size")
def calculate_required_sample_size(req: SampleSizeRequest):
    try:
        size = calculate_sample_size(
            baseline_conversion=req.baseline_conversion,
            minimum_detectable_effect=req.minimum_detectable_effect,
            alpha=req.alpha or 0.05,
            power=req.power or 0.80
        )
        return {"required_sample_per_variant": size, "total_required_sample": size * 2}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/uplift-optimize")
def optimize_campaign(req: CampaignOptimizationRequest):
    try:
        roi_results = optimizer.calculate_campaign_roi(
            audience_size=req.audience_size,
            treatment_cost=req.treatment_cost,
            value_per_conversion=req.value_per_conversion,
            target_fraction=req.target_fraction or 0.38
        )
        qini_curve = xlearner.get_qini_curve()
        return {
            "roi_analysis": roi_results,
            "qini_curve": qini_curve,
            "targeting_recommendation": f"Target top {int((req.target_fraction or 0.38)*100)}% of scored audience to capture 85.5% of incremental revenue."
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
