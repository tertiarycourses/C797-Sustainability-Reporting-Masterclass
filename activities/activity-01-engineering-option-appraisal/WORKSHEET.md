# Activity 1 Worksheet — Engineering Option Appraisal

## Exact procedure

1. Open `mock-data/mock-data.csv`. Confirm all monetary fields are SGD, reductions are annual, and risk/readiness use a 1–5 scale.
2. Calculate payback for each option: `payback years = capex_sgd / annual_savings_sgd`. Worked example for closed-loop water: `780,000 / 155,000 = 5.03 years`.
3. Convert each raw measure to a 1–5 decision score. Use these anchors: payback ≤3.5=5, ≤4.5=4, ≤5.5=3, ≤7=2, >7=1; readiness keeps its source score; compliance score=`6 - compliance_risk`; carbon and water scores rank options 5, 3, 1 from highest to lowest.
4. Apply weights: payback 25%, carbon 25%, water 15%, readiness 20%, compliance 15%. Formula: `weighted total = Σ(score × weight)`.
5. Stress-test by shifting 10 percentage points from payback to carbon. Record whether the ranking changes.
6. Endorse one option only if its weighted score is at least 3.5 and no evidence field is missing. Otherwise request more evidence.

## Results table

| Option | Payback | Base weighted score | Stress score | Evidence gap | Endorse / hold |
|---|---:|---:|---:|---|---|
| Closed-loop water |  |  |  |  |  |
| Waste-heat recovery |  |  |  |  |  |
| Alternative composite |  |  |  |  |  |

