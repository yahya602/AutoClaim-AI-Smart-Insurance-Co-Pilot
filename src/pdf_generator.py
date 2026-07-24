# PDF Report Generation using ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def create_claim_pdf(claim_id, customer_data, ai_analysis, manager_decision):
    """
    Final Approved Claim ki official PDF Report tayyar karta hai.
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "AutoClaim AI - Official Claims Processing Summary")
    pdf.line(100, 740, 500, 740)
    
    # Claim & Customer Details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 710, f"Claim ID: {claim_id}")
    pdf.drawString(100, 690, f"Customer Age: {customer_data['customer_age']}")
    pdf.drawString(100, 670, f"Claim Amount Requested: ${customer_data['claim_amount']}")
    
    # AI Assessment Results
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 630, "AI Co-Pilot Assessment:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 610, f"- Visual Damage: {ai_analysis['damage_level']} ({ai_analysis['confidence_score']}% Confidence)")
    pdf.drawString(100, 590, f"- Status Recommendation: {ai_analysis['llm_status']}")
    
    # Manager Action (HITL)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 550, "Human Manager Final Action:")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, 530, f"- Manager Decision: {manager_decision['manager_action']}")
    pdf.drawString(100, 510, f"- Final Approved Amount: ${manager_decision['final_approved_amount']}")
    pdf.drawString(100, 490, f"- Manager Remarks: {manager_decision['manager_notes']}")
    pdf.drawString(100, 470, f"- Timestamp: {manager_decision['processed_at']}")
    
    pdf.showPage()
    pdf.save()
    
    buffer.seek(0)
    return buffer