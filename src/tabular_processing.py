# Zaroori Libraries
import pandas as pd
from pypdf import PdfReader

def process_tabular_data(customer_dict):
    """
    Customer key parameters ko validate aur format karta hai.
    """
    claim_amount = customer_dict.get("claim_amount", 0)
    policy_limit = customer_dict.get("policy_limit", 0)
    
    risk_flag = False
    if claim_amount > policy_limit:
        risk_flag = True
        
    return {
        "claim_amount": claim_amount,
        "policy_limit": policy_limit,
        "over_limit_risk": risk_flag,
        "customer_age": customer_dict.get("age", 30)
    }

def extract_text_from_pdf(pdf_file):
    """
    PDF file se text extract karta hai.
    """
    try:
        reader = PdfReader(pdf_file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text() or ""
        return extracted_text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"