import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://backend:8000")

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
    business_id = st.text_input("Business ID (optional)")
    if uploaded_file:
        if st.button("Upload"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            data = {"business_id": business_id}
            resp = requests.post(f"{API_URL}/upload_invoice", files=files, data=data)
            if resp.ok:
                st.success("Uploaded")
                st.json(resp.json())
            else:
                st.error(resp.text)
