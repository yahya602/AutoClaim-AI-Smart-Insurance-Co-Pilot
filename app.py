import streamlit as st
import tempfile
import os

# Internal modules import kar rahe hain
from src.image_processing import predict_car_damage
from src.tabular_processing import process_tabular_data, extract_text_from_pdf
from src.text_processing import generate_llm_reasoning
from src.hitl_workflow import generate_xai_explanation, process_human_decision
from src.pdf_generator import create_claim_pdf

# Page Config Setup
st.set_page_config(page_title="AutoClaim AI Co-Pilot", layout="wide")

st.title("🚗 AutoClaim AI: Smart Insurance Co-Pilot")
st.caption("Multimodal Deep Learning & Human-In-The-Loop Claims Processing")

st.sidebar.header("📁 Step 1: Upload Claim Data")

# Input 1: Car Damage Image
uploaded_image = st.sidebar.file_uploader("Upload Accident Image", type=["jpg", "png", "jpeg"])

# Input 2: Claim PDF / Incident Statement
uploaded_pdf = st.sidebar.file_uploader("Upload Incident Report (PDF)", type=["pdf"])

# Input 3: Tabular Inputs
st.sidebar.subheader("Customer Details")
claim_amount = st.sidebar.number_input("Claim Amount ($)", min_value=100, value=2500)
policy_limit = st.sidebar.number_input("Policy Limit ($)", min_value=500, value=5000)
customer_age = st.sidebar.number_input("Customer Age", min_value=18, value=35)

if uploaded_image and st.sidebar.button("Run AI Co-Pilot Analysis"):
    # 1. Process Image with CNN
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_image.getvalue())
        tmp_img_path = tmp_file.name

    img_result = predict_car_damage(tmp_img_path)
    os.remove(tmp_img_path)
    
    # 2. Process Tabular Data
    tabular_input = {"claim_amount": claim_amount, "policy_limit": policy_limit, "age": customer_age}
    tabular_result = process_tabular_data(tabular_input)
    
    # 3. Extract Text from PDF
    pdf_text = "Accident on main highway due to slippery weather."
    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        
    # 4. LLM & Reasoning Analysis
    llm_output = generate_llm_reasoning(img_result, tabular_result, pdf_text)
    xai_output = generate_xai_explanation(img_result, tabular_result)
    
    # Save results in Streamlit Memory
    st.session_state['analysis'] = {
        "img_result": img_result,
        "tabular_result": tabular_result,
        "llm_output": llm_output,
        "xai_output": xai_output
    }

# Display Analysis if Available
if 'analysis' in st.session_state:
    data = st.session_state['analysis']
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Visual & Tabular Analysis")
        st.image(uploaded_image, width=300)
        st.write(f"**Damage Predicted:** {data['img_result']['damage_level']}")
        st.write(f"**CNN Model Confidence:** {data['img_result']['confidence_score']}%")
        
    with col2:
        st.subheader("💡 Explainable AI (XAI) & LLM Reasoning")
        st.info(data['llm_output']['reasoning_summary'])
        
        st.markdown("**Key Risk Factors:**")
        for factor in data['xai_output']['key_contributing_factors']:
            st.write(f"- {factor}")

    st.divider()
    # Step 2: Human-In-The-Loop Approval Workflow
    st.subheader("🛡️ Step 2: Human-in-the-Loop Approval (Manager Review)")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        action = st.selectbox("Select Action", ["APPROVED", "REJECTED", "MODIFIED"])
        final_payout = st.number_input("Final Approved Payout ($)", value=float(claim_amount))
    with m_col2:
        notes = st.text_area("Manager Review Remarks", "Claim details verified and matches damages.")
        
    if st.button("Finalize Decision & Generate Official PDF"):
        hitl_record = process_human_decision("CLM-9821", data['llm_output']['status'], action, notes, final_payout)
        
        st.success(f"Decision Recorded Successfully! Status: {action}")
        
        # PDF Generation
        pdf_bytes = create_claim_pdf("CLM-9821", data['tabular_result'], {
            "damage_level": data['img_result']['damage_level'],
            "confidence_score": data['img_result']['confidence_score'],
            "llm_status": data['llm_output']['status']
        }, hitl_record)
        
        st.download_button(
            label="📄 Download Official Signed PDF Report",
            data=pdf_bytes,
            file_name="AutoClaim_Official_Report.pdf",
            mime="application/pdf"
        )