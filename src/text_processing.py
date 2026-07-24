# LLM Logic Mock / API Wrapper for Hackathon
def generate_llm_reasoning(image_result, tabular_result, text_summary):
    """
    Teenon modalities ke inputs ko combine karke AI Reasoning Report banata hai.
    """
    
    # Prompt Construction (Prompt Engineering)
    prompt = f"""
    --- INSURANCE AI CO-PILOT ANALYSIS ---
    1. Visual Inspection (CNN): {image_result['damage_level']} (Confidence: {image_result['confidence_score']}%)
    2. Financial & Policy Data: Claim Amount ${tabular_result['claim_amount']} vs Policy Limit ${tabular_result['policy_limit']}
    3. Incident Statement: {text_summary}
    """
    
    # Rule-Based LLM Simulation (System Prompt + Reasoning)
    if tabular_result['over_limit_risk']:
        status = "REJECT_RECOMMENDED"
        reasoning = "Requested claim amount exceeds maximum policy coverage limit."
    elif "Severe" in image_result['damage_level'] and tabular_result['claim_amount'] < 1000:
        status = "FLAGGED_FOR_REVIEW"
        reasoning = "Mismatch: High physical damage predicted but claimed amount is suspiciously low."
    else:
        status = "APPROVE_RECOMMENDED"
        reasoning = "Damage visuals match incident description and fall within valid policy limits."

    explanation = f"""
    [AI Executive Summary]
    Recommended Action: {status}
    Key Finding: {reasoning}
    Visual Proof Match: High
    Policy Compliance: {'Failed' if tabular_result['over_limit_risk'] else 'Passed'}
    """
    
    return {
        "status": status,
        "reasoning_summary": explanation.strip()
    }