import pandas as pd
import numpy as np
import os

# 1. Generate Synthetic Tabular Dataset
np.random.seed(42)
n_samples = 200

data = {
    'claim_id': [f'CLM_{1000+i}' for i in range(n_samples)],
    'policy_holder_age': np.random.randint(18, 70, size=n_samples),
    'vehicle_age_years': np.random.randint(0, 15, size=n_samples),
    'claim_amount_requested': np.random.choice([15000, 35000, 75000, 150000, 300000], size=n_samples),
    'previous_claims_count': np.random.choice([0, 1, 2, 3], p=[0.6, 0.25, 0.1, 0.05], size=n_samples),
    'incident_type': np.random.choice(['Front Collision', 'Rear Collision', 'Parked Scrape', 'Rollover'], size=n_samples),
    'damage_severity': np.random.choice(['Minor', 'Moderate', 'Severe'], p=[0.5, 0.35, 0.15], size=n_samples),
    'ai_approval_recommendation': np.random.choice(['Approve', 'Manual Review', 'Reject'], p=[0.7, 0.2, 0.1], size=n_samples)
}

df = pd.DataFrame(data)
os.makedirs('dataset', exist_ok=True)
df.to_csv('dataset/claims_data.csv', index=False)
print("✅ 'dataset/claims_data.csv' successfully created with 200 rows!")

# 2. Generate Sample Text Report
os.makedirs('dataset/reports', exist_ok=True)
sample_text = """ACCIDENT INCIDENT REPORT
Claim ID: CLM_1000
Policy Coverage: Full Comprehensive

Incident Details:
Driver states that while reversing out of a parking slot, another vehicle hit the rear bumper. 
Damage is isolated to the rear plastic bumper and right taillight assembly.

Surveyor Recommendation:
Eligible for claim. Standard deductible applies."""

with open('dataset/reports/CLM_1000_report.txt', 'w') as f:
    f.write(sample_text)
print("✅ Sample text report created in 'dataset/reports/'!")