import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://backend:8000")

st.title("Tax Calculator & Invoice Upload")

menu = st.sidebar.selectbox("Choose", ["Tax Calculator", "Upload Invoice"])

if menu == "Tax Calculator":
    st.header("Compute tax")
    income = st.number_input("Income", min_value=0.0, format="%.2f")
    deductions = st.number_input("Deductions", min_value=0.0, format="%.2f")
    period = st.selectbox("Period", ["Monthly", "Yearly"])
    if st.button("Calculate"):
        resp = requests.post(f"{API_URL}/calculate_tax", json={"income": income, "deductions": deductions, "period": period})
        if resp.ok:
            st.json(resp.json())
        else:
            st.error(f"Error: {resp.text}")

if menu == "Upload Invoice":
    st.header("Upload an invoice (PDF/JPG/PNG)")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
    business_id = st.text_input("Business ID (required)")
    
    if uploaded_file:
        if not business_id.strip():
            st.warning("Business ID is required to upload a file.")
        else:
            # Send file and business_id to backend
            file_tuple = (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            resp = requests.post(
                f"{API_URL}/upload_invoice",
                files={"file": file_tuple},
                data={"business_id": business_id}
            )
            if resp.ok:
                st.success("Uploaded!")
                st.json(resp.json())
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")
