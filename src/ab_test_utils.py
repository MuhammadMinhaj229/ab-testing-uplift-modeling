import numpy as np
import scipy.stats as stats
from typing import Dict, Any

def run_chi_square_test(
    control_conversions: int,
    control_size: int,
    treatment_conversions: int,
    treatment_size: int,
    alpha: float = 0.05
) -> Dict[str, Any]:
    """
    Executes an exact Chi-Square test of independence on a 2x2 contingency table.
    
    Contingency table:
                   Converted | Not Converted
    Control:           c1    |   s1 - c1
    Treatment:         c2    |   s2 - c2
    """
    if control_size <= 0 or treatment_size <= 0:
        raise ValueError("Group sizes must be strictly positive integers.")
    if control_conversions < 0 or treatment_conversions < 0:
        raise ValueError("Conversions cannot be negative.")
    if control_conversions > control_size or treatment_conversions > treatment_size:
        raise ValueError("Conversions cannot exceed total group size.")

    ctrl_non = control_size - control_conversions
    treat_non = treatment_size - treatment_conversions

    table = np.array([
        [control_conversions, ctrl_non],
        [treatment_conversions, treat_non]
    ])

    chi2_stat, p_val, dof, expected = stats.chi2_contingency(table, correction=True)

    ctrl_rate = control_conversions / control_size
    treat_rate = treatment_conversions / treatment_size
    abs_lift = treat_rate - ctrl_rate
    rel_lift = (abs_lift / ctrl_rate) * 100 if ctrl_rate > 0 else 0.0

    # Pooled standard error for 95% confidence interval on difference of proportions
    se_diff = np.sqrt(
        (ctrl_rate * (1 - ctrl_rate) / control_size) +
        (treat_rate * (1 - treat_rate) / treatment_size)
    )
    z_crit = stats.norm.ppf(1 - (alpha / 2))
    ci_lower = abs_lift - (z_crit * se_diff)
    ci_upper = abs_lift + (z_crit * se_diff)

    significant = bool(p_val < alpha)

    recommendation = (
        "Statistically significant lift detected. Treatment variant outperforms control."
        if significant and abs_lift > 0
        else "No statistically significant difference detected at 95% confidence level."
        if not significant
        else "Statistically significant negative impact detected. Halt treatment immediately."
    )

    return {
        "statistic": round(float(chi2_stat), 4),
        "p_value": float(p_val),
        "significant": significant,
        "control_rate": round(float(ctrl_rate), 4),
        "treatment_rate": round(float(treat_rate), 4),
        "absolute_lift": round(float(abs_lift), 4),
        "relative_lift_pct": round(float(rel_lift), 2),
        "ci_95": [round(float(ci_lower), 4), round(float(ci_upper), 4)],
        "recommendation": recommendation
    }

def calculate_sample_size(
    baseline_conversion: float,
    minimum_detectable_effect: float,
    alpha: float = 0.05,
    power: float = 0.80
) -> int:
    """
    Computes required per-variant sample size for two-tailed hypothesis test.
    """
    p1 = baseline_conversion
    p2 = baseline_conversion * (1 + minimum_detectable_effect)
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    pooled_p = (p1 + p2) / 2
    numerator = (z_alpha * np.sqrt(2 * pooled_p * (1 - pooled_p)) + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2

    return int(np.ceil(numerator / denominator))
