# Human-In-The-Loop & Decision State Management

import datetime

def generate_xai_explanation(ai_prediction, tabular_data):
    """
    AI ke internal factors ko ek transparent explanation summary mein convert karta hai.
    """
    damage_level = ai_prediction['damage_level']
    confidence = ai_prediction['confidence_score']
    claim_amt = tabular_data['claim_amount']
    policy_lim = tabular_data['policy_limit']
    
    # Transparency Indicators (XAI Feature Importance Simulation)
    factors = []
    
    if confidence > 80:
        factors.append(f"Visual Model High Confidence ({confidence}%)")
    else:
        factors.append(f"Visual Model Low Confidence ({confidence}%) - Needs Manual Verification")
        
    if claim_amt <= policy_lim:
        factors.append(f"Claim Amount (${claim_amt}) is within Policy Limit (${policy_lim})")
    else:
        factors.append(f"CRITICAL: Claim Amount (${claim_amt}) EXCEEDS Policy Limit (${policy_lim})")
        
    explanation_breakdown = {
        "primary_factor": f"Predicted {damage_level}",
        "confidence_level": f"{confidence}%",
        "key_contributing_factors": factors
    }
    
    return explanation_breakdown


def process_human_decision(claim_id, ai_recommendation, manager_action, manager_notes="", final_payout=0):
    """
    Manager ke final action (Approve/Reject/Modify) ko record karta hai.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    final_record = {
        "claim_id": claim_id,
        "ai_recommendation": ai_recommendation,
        "manager_action": manager_action,  # Options: 'APPROVED', 'REJECTED', 'MODIFIED'
        "final_approved_amount": final_payout,
        "manager_notes": manager_notes,
        "processed_at": timestamp,
        "status": "COMPLETED"
    }
    
    return final_record